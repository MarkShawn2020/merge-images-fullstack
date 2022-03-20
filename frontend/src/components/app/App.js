import './App.css';
import { Button, Image, Slider, Spin, Switch, Upload } from "antd"
import Layout, { Content, Footer } from 'antd/lib/layout/layout';
import { useState, useRef, useEffect } from 'react';
import { LoadingOutlined, UploadOutlined } from "@ant-design/icons"
import ImgItem from '../img_item/img_item';

const HOST = "http://localhost:8000"
const DEFAULT_Y1 = 80
const DEFAULT_Y2 = 95
const MAX_IMAGES = 50

const axios = require('axios');

const antIcon = <LoadingOutlined style={{ fontSize: 72 }} spin />;


function App() {
  // 上传的文件列表
  const [fileList, setFileList] = useState([])
  // 渲染的图片的名称与在服务器上的url
  const [mergedImg, setMergedImg] = useState(null)
  // 基于是否上传完成，控制渲染与下载图片的按钮行为
  const [isUploaded, setUploaded] = useState(false)
  // 基于渲染是否完成，控制用户等待等交互行为
  const [isGenerating, setGenerating] = useState(false)
  // 切换省流或原话渲染模式，推荐省流，毕竟下载时都是超清的，渲染要快
  const [isLowMode, setLowMode] = useState(true)

  /**
   * 子组件控制
   * 为获取对子组件的自上而下控制，故使用ref数组，获取其内部imperativeHandler方法
   * 参考：https://stackoverflow.com/a/56063129/9422455
   */
  const refFiles = useRef([])
  // 每次状态更新后同步更新ref数组
  // TODO: 这里要确认一下，依赖是否可以只根据检测length
  useEffect(() => {
    refFiles.current = refFiles.current.slice(0, fileList.length)
  }, [fileList.length,
    // fileList.filter(f => f.response).map(f => f.response.url).join("-")
  ])

  const updateChildren = (i, j, abs) => {
    refFiles.current.forEach(ref => {
      // 重要：这里的写法跟其他地方的ref不同，其他要用ref.current，而这里是数组里的元素（已经用过一次current了），所以不需要再用ref.current去调用updateYi，这是不对的！
      ref.updateYi(i, j, abs, 0)
    })
  }
  const deleteChild = (index) => {
    setFileList(fileList => [...fileList.slice(0, index), ...fileList.slice(index + 1)])
  }
  const moveChild = (index, step) => {
    const N = fileList.length
    const s = step > 0 ? index : index + step < 0 ? 0 : index + step;
    const e = step < 0 ? index : index + step > N - 1 ? N - 1 : index + step;
    const newFileList = step > 0 ?
      [...fileList.slice(0, s), ...fileList.slice(s + 1, e + 1), fileList[s], ...fileList.slice(e + 1)] :
      [...fileList.slice(0, s), fileList[e], ...fileList.slice(s, e), ...fileList.slice(e + 1)]
    console.log({ index, step, old: fileList, new: newFileList });
    setFileList(newFileList)
  }

  /**
   * 上传控制
   * @param {} e 回调 {fileList, file, event}
   */
  const onResponseChange = e => {
    /**
     * 多次刷新中，会动态的返回fileList[, file, event]三种关键字，其中fileList一直有
     * 并且每次都要更新一下fileList，否则可能就接收不到后续的update了
     * 至于判断什么时候上传成功，要么可以通过看file.status是否为'done'，要么基于fileList的统计
     * 由于上传的照片数量并不会很多，直接基于统计判断isUploaded就可以
     */
    console.log(e);
    // - [Upload file.status is always being uploading · Issue #2423 · ant-design/ant-design](https://github.com/ant-design/ant-design/issues/2423)
    setFileList(e.fileList)
    if (e.fileList.every(file => file.status === "done")) {
      setUploaded(true)
    }
  }

  /**
   * 渲染生成
   * @param {*} use_raw 是否使用原画模式
   * @returns 
   */
  const onGenerate = async (use_raw) => {
    // fastapi的post接口，不用考虑param关键字，直接喂body数据即可
    setGenerating(true)
    const data = fileList.map((file, i) => {
      let name = file.response.filename
      if (use_raw) {
        name = name.replace("medium", "raw")
      }
      return {
        name,
        y1: refFiles.current[i].y1,
        y2: refFiles.current[i].y2,
      }
    })
    const res = await axios({
      method: "post",
      url: HOST + "/merge_imgs/",
      data
    })
    console.log({ use_raw, data, res });
    setMergedImg(res.data)
    setGenerating(false)
    return res.data
  }

  /**
   * 重置
   */
  const onReset = () => {
    setFileList([])
    setUploaded(false)
  }


  return (
    <div className="App">

      <Layout>
        <Content>
          <div id='body'>
            {/* 上传控制 开始*/}
            <div id="operates">
              <Switch id='lowModeSwitch' checkedChildren="省流" unCheckedChildren="原画" defaultChecked={isLowMode} onChange={setLowMode} />

              <Button id='resetBtn' danger onClick={onReset}>重置</Button>

              <Upload
                action={HOST + "/uploadfile?compress=" + isLowMode}
                onChange={onResponseChange}
                listType='picture'
                defaultFileList={[]}
                maxCount={MAX_IMAGES}
                multiple={true}
                fileList={fileList}
              >
                <Button icon={<UploadOutlined />}>上传</Button>
              </Upload>
            </div>
            {/* 上传控制 结束 */}

            {/* 拼接控制 开始 */}
            <div id="views_in">
              <div id="views_in_control">
                <Slider range reverse={false} defaultValue={[DEFAULT_Y1, DEFAULT_Y2]}
                  style={{ flexGrow: 1 }} onChange={e => {
                    // console.log({ e });
                    updateChildren(0, e[0], 1, 0);
                    updateChildren(1, e[1], 1, 0);
                  }} />
                <Button disabled={!isUploaded} onClick={() => onGenerate(false)}>渲染</Button>
                <Button onClick={async () => {
                  setGenerating(true)
                  const data = await onGenerate(true)
                  // const url = HOST + "/files/?filename=" + mergedImg.filename.replace("medium", "raw")
                  // await axios.get()
                  window.open(data.url)
                  setGenerating(false)
                }} disabled={!isUploaded}>下载</Button>
              </div>
              {
                fileList.map((file, i) => (
                  // 因为在uploading过程中，不断地更新，但可能还没读取到图片数据 
                  file.response && <ImgItem key={i} index={i} img={file.response.url} ref={el => refFiles.current[i] = el} deleteMe={deleteChild} moveMe={moveChild} />
                ))
              }
            </div>
            {/* 拼接控制 结束 */}

            {/* 渲染展示 开始 */}
            <div id="views_out" >
              <Spin spinning={isGenerating} indicator={antIcon}>
                {
                  mergedImg && <Image src={mergedImg.url} width={"100%"} preview={false} />
                }
              </Spin>
            </div>
            {/* 渲染展示 结束 */}
          </div>
        </Content>

        <Footer>
          南川字幕拼接系统V0.1 @2021-12-13
        </Footer>
        {/* <MyFooter /> */}
      </Layout>
    </div >
  );
}

export default App;


