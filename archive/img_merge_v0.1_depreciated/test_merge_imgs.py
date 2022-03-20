

if __name__ == "__main__":
    img_paths = [
        "./samples/sample1.png",
        "./samples/sample2.png"
    ]
    imgs = [Image.open(i) for i in img_paths]
    img_boxes = [ImgBox().from_pct(0, 0.05, 1, 0.95, *i.size).get_box()
                 for i in imgs]
    img_items = [ImgItem(i, j) for (i, j) in zip(imgs, img_boxes)]
    merge_imgs_and_save("merged_img.png", img_items)
