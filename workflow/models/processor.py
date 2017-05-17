# coding=utf-8
import json

import subprocess
from django.db import models
from basic import BasicModel
from parameter import Parameter
from io import InputChannel, OutputChannel
from hub.settings import BASE_DIR, MEDIA_ROOT



class Processor(BasicModel):
    name = models.CharField(max_length=140)
    algorithm_category_id = models.IntegerField(default=0)
    is_visualization = models.BooleanField(default=False)
    is_local = models.BooleanField(default=True)
    visualization_category = models.CharField(max_length=40)
    exec_file = models.FileField(upload_to='JAR/', null=True)
    category = models.ForeignKey('ProcessorCategory', related_name='processors')

    def drop(self):

        for cpara in self.configuredprocessor_set.all():
            cpara.delete()

        for parameter in self.params.all():
            parameter.parameter_input_object.delete()
            parameter.delete()

        for input in self.inputs.all():
            input.delete()

        for output in self.outputs.all():
            output.delete()

    def to_dict(self):
        # todo：这里可以使用Magic
        # image = {}
        category = self.category.to_sequence()
        if category == '':
            return
        result = {
            "id": self.pk,
            "name": self.name,
            "ac_id": self.algorithm_category_id,
            "visualization": self.is_visualization,
            "params": [param.to_dict(self.algorithm_category_id) for param in self.params.all() if not param.to_dict(self.algorithm_category_id) is None], # add ac_id
            "inputs": [input_channel.to_dict() for input_channel in self.inputs.all()],
            "outputs": [output_channel.to_dict() for output_channel in self.outputs.all()],
            "category": category,
            # "category": self.category.to_sequence()
            # "image": image,
        }
        return result

    def to_json(self):
        return json.dumps(self.to_dict())

    def runannotation(self, classname,jarpath):
        #classname=property  jarpath=/home/spark/Sql.jar
        cmd_header = "java -jar " + BASE_DIR + "/workflow/models/export_file/Annotation_new.jar"+" "+ classname+" " +jarpath
        print cmd_header
        proc = subprocess.Popen(cmd_header, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        proc.wait()
        a=proc.stdout.read()
        # print a
        if a == "404":
            return False
        attr={}
        readjson = json.loads(a)
        print readjson
        self.is_visualization = readjson.get("is_visualization")
        self.algorithm_category_id = readjson.get("algorithm_category")
        self.is_local = bool(readjson.get("is_local"))
        #self.save()
        attr["parameters"]=readjson.get("parameters")
        attr["inputs"]=readjson.get("inputs")
        attr["outputs"]=readjson.get("outputs")

        return attr

    @classmethod
    def create_from_json_dict(cls, attributes, **kwargs):
        # print attributes['is_visualization']

        processor = Processor(name=attributes['name'], exec_file=attributes['execFile'])
        category_path = attributes['category']
        categorys = category_path.split(">")
        # print categorys
        parent = None
        for category in categorys:
            child = ProcessorCategory.objects.get_or_create(parent=parent, name=Category.objects.get(
                category_id=int(category)).category_name,
                                                            category=Category.objects.get(category_id=int(category)))
            # child = ProcessorCategory.objects.get_or_create(parent=parent, name=category)
            if child[1] == 1:
                child[0].save()
            parent = child[0]
        # print categorys
        processor.category = parent
        # processor.exec_file = attributes['execFile']

        #put the parameters where?
        processor.save()
        classname = "com.property"
        jarpath = "/home/spark/"+ processor.exec_file.name
        # print jarpath
        dict=processor.runannotation(classname, jarpath)
        if dict == False:
            raise Exception("Not Found Property File")
        # print dict
        attributes.update(dict)
        try:
            processor.save()
        except Exception, e:
            print e
        # print processor
        # print attributes
        rollback = []
        try:
            for parameter_attributes in attributes['parameters']:
                # if parameter_attributes['label'] == '':
                #     continue
                # if parameter_attributes['parameterType'] == 'selection':
                #     parameter_attributes['choices'] = parameter_attributes['description'].split(",")
                a = Parameter.create_from_json_dict(parameter_attributes, processor=processor)
                rollback.append(a)
            # print attributes
            for input_attributes in attributes['inputs']:
                # if input_attributes['name'] == '':
                #     continue
                a = InputChannel.create_from_json_dict(input_attributes, processor=processor)
                rollback.append(a)
            for output_attributes in attributes['outputs']:
                # if output_attributes['name'] == '':
                #     continue
                a = OutputChannel.create_from_json_dict(output_attributes, processor=processor)
                rollback.append(a)
            # print categorys
        except Exception, e:
            processor.delete()
            for item in rollback:
                item.delete()
            raise e
        # processor.delete()
        # print attributes
        return processor


class ConfiguredProcessor(BasicModel):
    meta_processor = models.ForeignKey('Processor')
    workflow = models.ForeignKey('Workflow', related_name='processors')
    flow_id = models.CharField(max_length=30, default=0)
    loc_x = models.FloatField(default=0.0)
    loc_y = models.FloatField(default=0.0)

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            'id': self.meta_processor.id,
            'flow_id': self.flow_id,
            'loc_x' : self.loc_x,
            'loc_y' : self.loc_y,
            'inputs': [input_channel.id for input_channel in self.meta_processor.inputs.all()],
            'outputs': [output_channel.id for output_channel in self.meta_processor.outputs.all()],
        }

class ProcessorCategory(BasicModel):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=20, verbose_name=u'图标名称')
    category = models.ForeignKey("Category", related_name='ConfiguredCategory', default=None, null=True)
    parent = models.ForeignKey('self', related_name='children', default=None, null=True)

    def to_sequence(self):
        catetory = self.category
        if catetory.is_hidden:
            return ''
        # if not image.has_key(self.name) and catetory.picture_path.name is not None:
        #     image[self.name] = MEDIA_ROOT + catetory.picture_path.name
        path = self.name
        parent = self.parent
        while parent != None:
            catetory = parent.category
            if catetory.is_hidden:
                return ''

            path = parent.name + '>' + path
            parent = parent.parent

        return path

    @classmethod
    def delete_old(cls, **kwargs):
        assert 'children' in kwargs.keys()
        children = kwargs['children']
        assert children is not None

        if children == []:
            return 1

        for child in children:
            if child.delete_old(children=child.children.all()):
                for processor in child.processors:
                    processor.drop()
                    processor.delete()
            child.delete()

        return 0

class Category(BasicModel):
    category_id = models.IntegerField()
    category_name = models.CharField(max_length=20)
    is_hidden = models.BooleanField(default=False)
    picture_path = models.FileField(upload_to='Picture/', null=True)
    parent = models.ForeignKey('self', related_name='children', default=None, null=True)

    def to_dict(self):
        return {
            "id": self.category_id,
            'name': self.category_name,
            "isHidden": self.is_hidden,
            "children": [child.to_dict() for child in self.children.all() if child!= None],
            "picture": self.picture_path.name
        }

    @classmethod
    def create_from_json_dict(cls, attributes, **kwargs):
        assert 'parent' in kwargs.keys()
        parent = kwargs['parent']
        assert parent is not None
        assert 'image' in kwargs.keys()
        image = kwargs['image']
        # assert image is not None

        roll_back = []
        print int(attributes["id"])
        category = Category.objects.get_or_create(category_id=int(attributes["id"]))
        print attributes

        if category[1] == 1:
            category[0].category_name=attributes["name"]
            category[0].is_hidden=attributes["isHidden"]
            category[0].parent=parent
            category[0].picture_path = image
            category[0].save()

        try:
            for child in attributes["children"]:
                a = Category.create_from_json_dict(child, parent=category[0], image=image)
                roll_back.append(a)
        except Exception, e:
            if category[0].category_id != -1:
                category[0].delete()
            for item in roll_back:
                item.delete()
            raise e
        return category

    @classmethod
    def delete_old(cls, **kwargs):
        assert 'children' in kwargs.keys()
        children = kwargs['children']
        assert children is not None

        if children == []:
            return

        for child in children:
            # child.delete_old(children=child.children.all())
            child.delete()
