import os
import json
import subprocess
import numpy as np
import pandas as pd
from skimage.measure import find_contours
import base64
import matplotlib.pyplot as plt

#========================= preset ============================
json_file='E:\data\Shrimp size.v3i.coco-segmentation\\train\\_annotations.coco.json'
img_folder='E:\\data\\Shrimp size.v3i.coco-segmentation\\train'
json_save_folder='E:\data\Shrimp size.v3i.coco-segmentation\\train\\seg_label'
classification=["Shrimp","Shrimp","circle"]
#========================= function ===========================
class pic_attribute:
    pass
class shapes_attribute:
    pass
class myfun():
    def __init__(self,file):
        self.file=file
        with open(self.file) as f:
            self.data = json.load(f)
            self.version ="5.3.1"               #(data['info'])['version']
            self.categories =self.data['categories']
            self.images=self.data['images']
            self.annotations=self.data['annotations']
            
    def select_class(self,id):
        return classification[id]
    def id_sort(self):
        id_dict=dict()
        for i in self.images:
            if i['id'] not in id_dict:
                pic=pic_attribute()
                pic.id=i['id']
                pic.name=i['file_name']
                pic.size=[i['height'],i['width']]
                id_dict[i['id']]=pic
        return id_dict
            # self.id_dict[i['id']]=i['file_name']
    def collect_json_shape(self):
        shape_list=[]
        # for image,annotation in zip(self.images,self.annotations):
        #     shapes=shapes_attribute()
        #     # print("annotation: ",annotation)
        #     # print("{:-^50s}".format("Split Line"))
        #     shapes.image_id=annotation['image_id']
        #     shapes.label=annotation['category_id']
            
        #     self.file_name=image['file_name']
        #     self.wid=image['width']
        #     self.hei=image['height']
        #     self.dict_obj=dict()
        #     self.img_id=annotation['image_id']
        #     self.class_seg=annotation['category_id']
        #     self.class_seg=self.select_class(self.class_seg)
        #     # print("class:",self.class_seg)
        #     self.points=annotation['segmentation']
        #     step=2
        #     self.point=[self.points[0][i:i+step] for i in range(0,len(self.points[0]),2)]

        #     shapes.point=self.point
        #     shapes.group_id=None
        #     shapes.description=""
        #     shapes.shape_type="polygon"
            
        #     self.dict_obj["label"]=self.class_seg
        #     self.dict_obj["points"]=self.point
        #     self.dict_obj["group_id"]=None
        #     self.dict_obj["description"]=""
        #     self.dict_obj["shape_type"]="polygon"
        #     self.dict_obj["flags"]={}
        #     # print("class:",self.dict_obj)
        #     file_list.append(self.file_name)
        #     # shape_list.append(self.dict_obj)
        #     size_list.append([self.wid,self.hei])
        #     shape_list.append(shapes)
        # print(dict_list)

        #-----shapes
            #-----image_id
            #-----label
            #-----point
            #-----group_id
            #-----description
            #-----shape_type
            #-----flags
        for annotation in self.annotations:
            shapes=shapes_attribute()
            shapes.image_id=annotation['image_id']
            shapes.label=classification[annotation['category_id']]

            # self.img_id=annotation['image_id']
            # self.class_seg=annotation['category_id']
            self.points=annotation['segmentation']
            step=2
            self.point=[self.points[0][i:i+step] for i in range(0,len(self.points[0]),2)]
            shapes.point=self.point
            shapes.group_id=None
            shapes.description=""
            shapes.shape_type="polygon"
            shapes.flags={}
            shape_list.append(shapes)
        return shape_list

        # return file_list,shape_list,size_list,self.version,self.img_id
        # point_x=[i[0] for i in point]
        # point_y=[i[1] for i in point]
        # plt.plot(point_x,point_y)
        # plt.show()
    def build_shape_dict(self,shape_):
        _dict=dict()
        _dict['label']=shape_.label
        _dict['points']=shape_.point
        _dict['group_id']=shape_.group_id
        _dict['description']=shape_.description
        _dict['shape_type']=shape_.shape_type
        _dict['flags']=shape_.flags
        return _dict
    def put_to_json(self,shape_list,file_name,hei,wid):
        # _dict=dict()
        # _dict["version"]=str(version)
        # _dict["flags"]={}
        # _dict["shapes"]=shape_list
        # _dict["imagePath"]=file_name
        # with open(file_name, "rb") as f:
        #     imageData = f.read()
        #     imageData = base64.b64encode(imageData).decode("utf-8")
        # _dict["imageData"]=imageData
        # _dict["imageHeight"]=hei
        # _dict["imageWidth"]=wid
        # head,tail=os.path.split(file_name)
        # json.dump(_dict,open(head+'.json','w'),indent=4)
        
        _dict=dict()
        _dict["version"]=str(self.version)
        _dict["flags"]={}
        _dict["shapes"]=shape_list
        _dict["imagePath"]=file_name
        file_path=os.path.join(img_folder,file_name)
        with open(file_path, "rb") as f:
            imageData = f.read()
            imageData = base64.b64encode(imageData).decode("utf-8")
        _dict["imageData"]=imageData
        _dict["imageHeight"]=hei
        _dict["imageWidth"]=wid
        # head,tail=os.path.split(file_name)
        file_name=file_name[:-4]
        # print("head:",head)
        json.dump(_dict,open(os.path.join(json_save_folder,file_name)+'.json','w'),indent=4)
        
#========================= main ===========================
if __name__ == "__main__":

    # dict_obj,file_list,shape_list,wid,hei,version=
    f=myfun(json_file)
    id_att=f.id_sort()
    shape_list=f.collect_json_shape()
    shape_dict=dict()
    for i in shape_list:
        one_of_shape= f.build_shape_dict(i)
        # print(one_of_shape)

        if i.image_id not in shape_dict:
            shape_dict[i.image_id]=[one_of_shape]
        else:
            list_dict=shape_dict[i.image_id]
            list_dict.append(one_of_shape)
            shape_dict[i.image_id]=list_dict
            # print(shape_dict[i.image_id])
        # print("{:-^50s}".format("Split Line"))   
    # print(len(shape_dict))
    for num in range(len(shape_dict)):
        att=id_att[num]
        
        # head,tail=os.path.split(att.name[:-4])
        # print(att.name[:-4])
        f.put_to_json(shape_dict[num],att.name,att.size[0],att.size[1])
        # print(id_att[num].)
        # f.put_to_json(id_att[num],)
    # file_list,shape_list,size_list,version,img_id=f.collect_json_shape()
    # print(shape_list) 
    
    # print(file_list)
    # print("{:-^50s}".format("Split Line"))
    # print(shape_list)
    # print("{:-^50s}".format("Split Line"))
    # print(size_list)
    # print("{:-^50s}".format("Split Line"))
    # print(version)
    # print(f.categories[])

    # plt.show()  
    # print(image)
    # print(images,info,annotation)
    # print("\n")    
    # filename=images['file_name']
    
    # print(file_name)
