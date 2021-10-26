# import torch
# import torchvision.transforms as transforms
from PIL import Image
# from model import LeNet5
#
def predict(img_path):
    # transform = transforms.Compose(
    #     [transforms.Resize((32,32)),
    #      transforms.ToTensor(),
    #      transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5))
    #     ])
    #
    # classes = ('liangtang','sankuaiwa','sidakuai','wuhua','xiangxing','zheng')
    #
    # net = LeNet5()
    # net.load_state_dict(torch.load('./app/lenet.pth'))
    #
    im = Image.open(img_path).convert('RGB')
    print(im)
    # im = transform(im) #[C,H,W]
    # im = torch.unsqueeze(im,dim=0)#加一个纬度，[N,C,H,W]

    # with torch.no_grad():
    #     outputs = net(im)
    #     predict = torch.max(outputs,dim=1)[1].data.numpy()
    # print(classes[int(predict)])
    #
    return str(124)


