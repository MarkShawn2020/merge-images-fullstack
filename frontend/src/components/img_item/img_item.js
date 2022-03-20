import { ArrowDownOutlined, ArrowUpOutlined, LockOutlined, UnlockOutlined } from "@ant-design/icons";
import { Image, Button } from "antd"
import React, { useState, useRef, useImperativeHandle, forwardRef } from "react";

var imgBlank = document.createElement('img')
imgBlank.src = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'

export const ImgLine = ({ i, y1, y2, setDeltaY }) => {
    const refLastY = useRef(0)

    const onDragStart = (e) => {
        console.log("start dragging");
        refLastY.current = e.clientY;
        console.log({ yStart: refLastY.current });
        e.dataTransfer.setDragImage(imgBlank, 0, 0); // https://stackoverflow.com/a/54916283/9422455

    }

    const onDragEnd = (e) => {
        console.log("end dragging");
    }

    const onDrag = (e) => {
        /**
         * 坐标Y下降时，是指往上升，此时要转变成负数
         */
        if (e.clientY === 0) {
            console.log({ curY: e.clientY });
            return
        }
        const deltaY = e.clientY - refLastY.current
        setDeltaY(deltaY, i)
        refLastY.current = e.clientY
        console.log({ curY: e.clientY, deltaY });
    }

    const onDrop = (e) => {
    }
    let style = {
        position: "absolute", top: y1 + "%", left: 0, width: "100%",
        "height": y2 - y1 + "%", background: "gray", opacity: 0.7
    }
    if (i === 1) {
        style.borderTop = "1px solid red"
    } else {
        style.borderBottom = "1px solid red"
    }

    return (
        <div
            draggable={true}
            onDragStart={onDragStart}
            onDragEnd={onDragEnd}
            onDrag={onDrag}
            onDrop={onDrop}
            style={style} />
    )
}

// https://stackoverflow.com/a/59554079/9422455
// Hook
const useKeyPress = (targetKey) => {
    // State for keeping track of whether key is pressed
    const [keyPressed, setKeyPressed] = React.useState(false)

    // If pressed key is our target key then set to true
    const downHandler = ({ key }) => {
        // console.log({ keyDown: key });
        if (key === targetKey) {
            setKeyPressed(true)
        }
    }

    // If released key is our target key then set to false
    const upHandler = ({ key }) => {
        if (key === targetKey) {
            setKeyPressed(false)
        }
    }

    // Add event listeners
    React.useEffect(() => {
        window.addEventListener('keydown', downHandler)
        window.addEventListener('keyup', upHandler)
        // Remove event listeners on cleanup
        return () => {
            window.removeEventListener('keydown', downHandler)
            window.removeEventListener('keyup', upHandler)
        }
    }, []) // Empty array ensures that effect is only run on mount and unmount

    return keyPressed
}

const ImgItem = ({ index, img, deleteMe, moveMe }, ref) => {

    const Y1 = index === 0 ? 5 : 80;
    const Y2 = 95;
    const [y1, setY1] = useState(Y1)
    const [y2, setY2] = useState(Y2)
    const [fixed, setFixed] = useState(index === 0)

    const isCmdKeyDown = useKeyPress("Meta") // command key

    /**
     * 
     * @param {*} i 
     * @param {*} j 
     * @param {*} self 给子组件自己调用自己的特权
     * @returns 
     */
    const updateYi = (i, j, abs, self) => {
        if (fixed && !self) return;
        let s = abs === 1 ? j : (i === 0 ? y1 : y2) + j;
        s = s > 100 ? 100 : s < 0 ? 0 : s;
        i === 0 ? setY1(s) : setY2(s);
    }

    useImperativeHandle(ref, () => ({
        updateYi,
        y1,
        y2
    }))

    const m = isCmdKeyDown * 9 + 1


    return (
        <div style={{ display: "flex" }}>
            <div style={{ display: "flex", flexDirection: "column" }}>
                <div style={{ display: "inline-flex", justifyContent: "space-around" }}>
                    <Button onClick={() => updateYi(0, m, 0, 1)}>+</Button>
                    <Button onClick={() => updateYi(0, -m, 0, 1)}>-</Button>
                </div>
                <div style={{ display: "inline-flex", justifyContent: "space-around" }}>
                    <Button onClick={() => updateYi(1, m, 0, 1)}>+</Button>
                    <Button onClick={() => updateYi(1, -m, 0, 1)}>-</Button>
                </div>
                <Button size="small" danger={fixed} onClick={() => setFixed(!fixed)}>
                    {fixed ? <LockOutlined /> : <UnlockOutlined />}</Button>


                <div style={{ display: "inline-flex", justifyContent: "space-around" }}>
                    <Button size="small" onClick={() => { moveMe(index, -1) }}><ArrowUpOutlined /> </Button>
                    <Button size="small" onClick={() => { moveMe(index, 1) }}><ArrowDownOutlined /> </Button>
                </div>

                <Button danger onClick={() => { deleteMe(index) }}>delete</Button>
            </div>

            <div style={{ position: "relative" }}>
                <Image src={decodeURIComponent(img)} width={"100%"} preview={false} />
                {/* TODO: 根据线调节！ */}
                <ImgLine i={0} y1={0} y2={y1} setDeltaY={() => { }} />
                <ImgLine i={1} y1={y2} y2={100} setDeltaY={() => { }} />
            </div>
        </div>

    )
}

export default forwardRef(ImgItem)