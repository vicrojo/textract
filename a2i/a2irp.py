import json
import re


class Word:
    def __init__(self, block, blockMap):
        self._block = block
        self._id = block['id']
        self._text = ""
        if(block['text']):
            self._text = block['text']

    def __str__(self):
        return self._text

    @property
    def id(self):
        return self._id

    @property
    def text(self):
        return self._text

    @property
    def block(self):
        return self._block
        
class Field:
    def __init__(self, block, blockMap):
        self._key = None
        self._value = None

        for item in block['relationships']:
            if(item["type"] == "CHILD"):
                self._key = FieldKey(block, item['ids'], blockMap)
            elif(item["type"] == "VALUE"):
                for eid in item['ids']:
                    vkvs = blockMap[eid]
                    if 'VALUE' in vkvs['entityTypes']:
                        if('relationships' in vkvs):
                            for vitem in vkvs['relationships']:
                                if(vitem["type"] == "CHILD"):
                                    self._value = FieldValue(vkvs, vitem['ids'], blockMap)
    def __str__(self):
        s = "\nField\n==========\n"
        k = ""
        v = ""
        if(self._key):
            k = str(self._key)
        if(self._value):
            v = str(self._value)
        s = s + "Key: {}\nValue: {}".format(k, v)
        return s

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value


class FieldKey:
    def __init__(self, block, children, blockMap):
        self._block = block
        self._confidence = block['confidence']
        self._id = block['id']
        self._text = ""
        self._content = []

        t = []

        for eid in children:
            wb = blockMap[eid]
            if(wb['blockType'] == "WORD"):
                w = Word(wb, blockMap)
                self._content.append(w)
                t.append(w.text)

        if(t):
            self._text = ' '.join(t)

    def __str__(self):
        return self._text

    @property
    def confidence(self):
        return self._confidence


    @property
    def id(self):
        return self._id

    @property
    def content(self):
        return self._content

    @property
    def text(self):
        return self._text

    @property
    def block(self):
        return self._block

class FieldValue:
    def __init__(self, block, children, blockMap):
        self._block = block
        self._confidence = block['confidence']
        self._id = block['id']
        self._text = ""
        self._content = []

        t = []

        for eid in children:
            wb = blockMap[eid]
            if(wb['blockType'] == "WORD"):
                w = Word(wb, blockMap)
                self._content.append(w)
                t.append(w.text)

        if(t):
            self._text = ' '.join(t)

    def __str__(self):
        return self._text

    @property
    def confidence(self):
        return self._confidence

    @property
    def id(self):
        return self._id

    @property
    def content(self):
        return self._content

    @property
    def text(self):
        return self._text
    
    @property
    def block(self):
        return self._block

class A2IDocument:

    def __init__(self, a2i_response):

        self.a2i_response = a2i_response

        self.blockMap  = {}
        self.a2i_updated_fields = {}
        self.a2i_blocks = None
        
        self._parse()

    def _parse(self):
        
        self.a2i_blocks = self.a2i_response['humanAnswers'][0]['answerContent']['AWS/Textract/AnalyzeDocument/Forms/V1']['blocks']               
        
        for block in self.a2i_blocks:
                if('blockType' in block and 'id' in block):
                    self.blockMap[block['id']] = block
       
        for block in self.a2i_blocks:
            if block['blockType'] == 'KEY_VALUE_SET':
                if 'KEY' in block['entityTypes']:
                    f = Field(block, self.blockMap)
                    self.a2i_updated_fields[str(f.key)] = str(f.value)
                    
    def get_fields(self):            
        return self.a2i_updated_fields
    
    def get_field_by_key(self, key):
        field = None
        if((self.a2i_updated_fields is not None) and str(key) in self.a2i_updated_fields):
            field = self.a2i_updated_fields[str(key)]
        return field


        





