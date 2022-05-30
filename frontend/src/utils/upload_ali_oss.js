import OSS from 'ali-oss';
import moment from 'moment';
import os


const loadClient = async () => {
    return new OSS({
        region: 'oss-cn-hangzhou',
        // stsToken: '<Your securityToken>',
        accessKeyId: os.environ["ALI_AK"],
        accessKeySecret: os.environ["ALI_SK"],
        bucket: 'mark-vue-oss'
    });
};

export const putBlob = async ({ file }) => {
    const client = await loadClient();
    try {
        //object-name可以自定义为文件名（例如file.txt）或指定目录（例如abc/test/file.txt）的形式，实现将文件上传至当前Bucket或Bucket下的指定目录。
        //client.put('object-name', 'local-file')
        // key要唯一 加uuid和时间戳毫秒级
        const key = moment.unix(moment()) / 1000 + "-" + file.name
        let result = await client.put(key, file);
        console.log(result);
        return result
    } catch (e) {
        console.log(e);
    }
};

// 作者：汤姆夹克
// 链接：https://juejin.cn/post/6844904121934282766
// 来源：稀土掘金
// 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
