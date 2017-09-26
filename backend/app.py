import boto3
import os,sys
import json
import timeit

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

import requests

reko = boto3.client('rekognition')

def create_collection(CollectionIdName=None):
    if not CollectionIdName:
        raise AssertionError
    else:
        # reko.create_collection(CollectionId='test')
        reko.create_collection(CollectionId=CollectionIdName)

def list_all_collections():
    response = reko.list_collections()
    print response

def list_all_images_in_collection(CollectionId='test'):
    response = reko.list_faces(CollectionId=CollectionId)
    return response

def image_add_code(name, CollectionId='test'):
    print("adding %s" %(name))
    import base64
    encoded_string = ""
    with open("%s.jpeg" %(name), "rb") as image_file:
        # encoded_string = base64.b64encode(image_file.read())
    # import pdb; pdb.set_trace()
        print request.get_json()
        response =  reko.index_faces(
            CollectionId=CollectionId,
            Image={
                'Bytes': image_file.read()
            },
            DetectionAttributes=[
                'DEFAULT',
            ],
            ExternalImageId=name
        )
    # print response
    print ("added %s" %(name))

def add_images_to_collection():
    import base64
    image_add_code("gangadhar")
    image_add_code("shaktimaan")


# response = client.index_faces(
#     CollectionId='string',
#     Image={
#         'Bytes': b'bytes',
#         'S3Object': {
#             'Bucket': 'string',
#             'Name': 'string',
#             'Version': 'string'
#         }
#     },
#     ExternalImageId='string',
#     DetectionAttributes=[
#         'DEFAULT'|'ALL',
#     ]
# )

def test_images(CollectionId='test'):
    testset = os.listdir('testimages')
    print testset
    for image in testset:
        response = reko.search_faces_by_image(
            CollectionId=CollectionId,
            Image={
                'Bytes': open(os.path.join('testimages', image), 'rb').read(),
            },
            MaxFaces=1,
        )
        print response
        if not response['FaceMatches']:
            print("failt to find match for : %s" %(image))
        else:
            print("most probably matched %s for image: %s" %(response['FaceMatches'][0]['Face']['ExternalImageId'],
                                                             image))

def test_image_via_api(image, CollectionId='test'):
    response = reko.search_faces_by_image(
        CollectionId=CollectionId,
        Image={
            'Bytes': open(os.path.join('testimages', image), 'rb').read(),
        },
        MaxFaces=1,
    )
    print response
    if not response['FaceMatches']:
        print("failt to find match for : %s" % (image))
    else:
        print("most probably matched %s for image: %s" % (response['FaceMatches'][0]['Face']['ExternalImageId'],
                                                          image))

def upload_all_images_to_collection(CollectionId='test'):
    # lis = json.load(open("data.json", "r").read())
    with open('data.json') as data_file:
        lis = json.load(data_file)
    for ele in lis:
        name = ele["name"]
        imageURL = ele["image"]
        print("adding %s" % (name))
        # import  pdb; pdb.set_trace()
        try:
            response = reko.index_faces(
                CollectionId=CollectionId,
                Image={
                    'Bytes': requests.get(imageURL).content
                },
                DetectionAttributes=[
                    'DEFAULT',
                ],
                ExternalImageId=name.replace(" ","__")
            )
            print ("added %s" % (name))
        except:
            # print(e)
            print "Unexpected error:", sys.exc_info()[0]
            print("failed to upload image: %s for %s" %(imageURL, name))

#
if __name__=='__main__':
    # create_collection()
    print("reko tests")
    # list_all_collections()
    # list_all_images_in_collection()
    # add_images_to_collection()
    # list_all_images_in_collection()
    # test_images()
    # upload_all_images_to_collection()
    app.run()

@app.route('/api/match_faces', methods=['POST'])
def test_face_match():
    imageURI = request.get_json().get('imageURI', None)
    imageURI = imageURI.split(',')[1]
    response = reko.search_faces_by_image(
        CollectionId='test',
        Image={
            'Bytes': imageURI.decode('base64'),
        },
        MaxFaces=1,
    )
    if not response['FaceMatches']:
        print("failt to find match")
    else:
        print("most probably matched %s for image" % (response['FaceMatches'][0]['Face']['ExternalImageId']))
    print(response)
    return jsonify(response)

@app.route('/api/match_faces_detailed', methods=['POST'])
# @app.route('/api/match_faces_detailed/', methods=['POST'])
@app.route('/api/match_faces_detailed/<collection_id>', methods=['POST'])
def test_face_match_huge(collection_id="test"):
    print(collection_id)
    start_time = timeit.default_timer()
    imageURI = request.get_json().get('imageURI', None)
    imageURI = imageURI.split(',')[1]
    imgBytes = imageURI.decode('base64')
    print("time spend on imageURI processing %f " %(timeit.default_timer() - start_time))


    start_time = timeit.default_timer()
    details = reko.detect_faces(
        # CollectionId=CollectionId,
        Image={
            'Bytes': imgBytes,
        },
        Attributes=['ALL']
    )
    print("time spend on detecting face API %f " %(timeit.default_timer() - start_time))


    start_time = timeit.default_timer()
    matches = reko.search_faces_by_image(
        CollectionId=collection_id,
        Image={
            'Bytes': imgBytes,
        },
        MaxFaces=1,
    )
    print("time spend on matching face API %f " %(timeit.default_timer() - start_time))

    start_time = timeit.default_timer()
    # matches = response
    if not matches['FaceMatches']:
        print("no match for image")
        # matches = {}
    else:
        print("most probably matched %s" % (matches['FaceMatches'][0]['Face']['ExternalImageId']))
    # print response
    resp = matches

    resp["FaceDetails"] = details['FaceDetails'][0] #put the face details for the most prominent face
    print("time spend on postprocessing %f " %(timeit.default_timer() - start_time))

    return jsonify(resp)

@app.route('/api/add_faces_crowd', methods=['PUT'])
def add_faces_to_crowdsource_collection():
    start_time = timeit.default_timer()
    request_json = request.get_json()
    imageURI = request_json.get('imageURI', None)
    imageURI = imageURI.split(',')[1]
    imgBytes = imageURI.decode('base64')
    name = request_json.get('name')
    print("time spend on preprocessing %f " %(timeit.default_timer() - start_time))

    start_time = timeit.default_timer()
    response =  reko.index_faces(
        CollectionId="crowdsource",
        Image={
            'Bytes': imgBytes
        },
        DetectionAttributes=[
            'DEFAULT',
        ],
        ExternalImageId=name.replace(" ","__")
        )
    print("time spend on preprocessing %f " %(timeit.default_timer() - start_time))
    return jsonify(response)


@app.route('/api/get_faces')
def get_all_faces():
    return jsonify(list_all_images_in_collection())

@app.route('/')
def hello_world():
    return 'Hello, World!'