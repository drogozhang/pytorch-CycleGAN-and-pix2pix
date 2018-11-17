import os
import cv2
from options.test_options import TestOptions
from data import CreateDataLoader
from models import create_model
from util.visualizer import save_images
from util import html



def main(style):

    opt = TestOptions().parse()

    opt.dataroot = "datasets/own_data/testA"

    # four styles
    # opt.name = "style_ink_pretrained"
    # opt.name = "style_monet_pretrained"
    # opt.name = "style_cezanne_pretrained"
    # opt.name = "style_ukiyoe_pretrained"
    # opt.name = "style_vangogh_pretrained"


    # set original img size
    original_img = cv2.imread(opt.dataroot+"/temp.jpg")
    original_img_shape = tuple([item for item in original_img.shape[:-1]][::-1])

    opt.name = "style_%s_pretrained" % style
    # 不可更改
    opt.model = "test"

    cv2.imread("temp.jpg")

    opt.nThreads = 1   # test code only supports nThreads = 1
    opt.batchSize = 1  # test code only supports batchSize = 1
    opt.serial_batches = True  # no shuffle
    opt.no_flip = True  # no flip
    opt.display_id = -1  # no visdom display

    # need to overwrite 8-27 这边可以不要
    data_loader = CreateDataLoader(opt)
    dataset = data_loader.load_data()

    # create model
    model = create_model(opt)
    model.setup(opt)

    # create website
    # website没什么用，但是作者把保存图片写到了web_dir里面了，我就没有修改。

    web_dir = os.path.join(opt.results_dir, opt.name, '%s_%s' % (opt.phase, opt.which_epoch))
    print("web_dir", web_dir)
    webpage = html.HTML(web_dir, 'Experiment = %s, Phase = %s, Epoch = %s' % (opt.name, opt.phase, opt.which_epoch))
    print("webpage", webpage)
    # exit()

    # test
    for i, data in enumerate(dataset):
        # i is index enumerate生成，很简单的
        # type of data is dict
        # one key is A， A is a tensor which size is ([1, 3, 256, 256]), another is A_path which type is str. from the read path (include the name)
        # i. e. datasets/own_data/testA/2test.jpg
        # default how_many is 50 : 一个数据集中只能处理 50 张照片

        # need to overwrite  "data"
        # data 的形状和其一样，然后外面改写一个监听，应该就可以了
        if i >= opt.how_many:
            break
        model.set_input(data)

        model.test()
        visuals = model.get_current_visuals()
        img_path = model.get_image_paths()
        if i % 5 == 0:
            print('processing (%04d)-th image... %s' % (i, img_path))
        save_images(webpage, visuals, img_path, aspect_ratio=opt.aspect_ratio, width=opt.display_winsize)

        generate_img = cv2.imread("results/generate_images/" + "temp.png")
        reshape_generate_img = cv2.resize(generate_img, original_img_shape, interpolation=cv2.INTER_CUBIC)

        cv2.imwrite("results/generate_images/" + "temp.png", reshape_generate_img)


if __name__ == '__main__':
    style = "ink"
    main(style)
