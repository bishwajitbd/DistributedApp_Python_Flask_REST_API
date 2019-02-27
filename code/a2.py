"""
 * a1.py
 * REST API
 * Assignment 2

 * Revision History
 * Bishwajit Barua, 2018.09.22: Created
"""
from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
import datetime

app=Flask(__name__)
app.secret_key="bbarua"
api=Api(app)

#Endpoing of authenticate /auth  example : http://127.0.0.1:5000/auth
jwt=JWT(app, authenticate, identity)   #/auth

# In memory variable declear
musics= []
review=[]
music_id=1
commentID=1
dateToday=datetime.datetime.now()

# Class for specific music related api request
class Music(Resource):
    @jwt_required()
    def get(self, _id):
        music= next(filter(lambda x: x['_id']==_id, musics), None)
        reviews=[]
        for rev in review:
            if rev['_id']== _id:
                reviews.append(rev)

        return {'music': music, 'review': reviews}, 200 if music else 404

    @jwt_required()
    def delete(self, _id):
        global musics
        global review
        musics=list(filter(lambda x: x['_id']!=_id, musics))
        review=list(filter(lambda x: x['_id']!=_id, review))
        return {'message' : 'Song #'+_id+' deleted'}

    @jwt_required()
    def put(self, _id):
        data = request.get_json(force=True)
        music = next(filter(lambda x: x['_id']==_id, musics), None)
        if music is None:
            music={'_id': _id, 'Album':data['Album'],'Title':data['Title'],'Artist':data['Artist']
            ,'Download':'“https://allmusic.com/music/download/IndiansEnnio.mp3”'
            ,'EntryDate':str(dateToday), 'review':[]}
            music.append(music)
        else:
            music.update(data)
        return music

    @jwt_required()
    def patch(self, _id):
        data = request.get_json(force=True)
        music = next(filter(lambda x: x['_id']==_id, musics), None)
        if music is None:
            music={'_id': _id, 'Album':data['Album'],'Title':data['Title'],'Artist':data['Artist']
            ,'Download':'“https://allmusic.com/music/download/IndiansEnnio.mp3”'
            ,'EntryDate':str(dateToday), 'review':[]}
            music.append(music)
        else:
            music.update(data)
        return music

# Class for all music records related api request
class MusicAll(Resource):
    @jwt_required()
    def post(self):
        global music_id
        data= request.get_json(force=True)
        music={'_id':str(music_id), 'Album':data['Album'],'Title':data['Title'],'Artist':data['Artist']
        ,'Download':'“https://allmusic.com/music/download/IndiansEnnio.mp3”'
        ,'EntryDate':str(dateToday)}
        music_id=music_id+1
        musics.append(music)
        return musics, 201

    @jwt_required()
    def get(self):
        return {'musics': musics}

# Class for specific review  records related api request
class AllReview(Resource):
    @jwt_required()
    def post(self, _id):
        global commentID
        data= request.get_json(force=True)
        music= next(filter(lambda x: x['_id']==str(_id), musics), None)
        if music is not None:
            reviews={'_id': _id, 'commentID': str(commentID), 'commenter': data['commenter'], 'comment': data['comment'], 'entryDate': str(dateToday)}
            commentID=commentID+1
            review.append(reviews)
        return review, 201

    @jwt_required()
    def get(self, _id):
        global review
        reviews = next(filter(lambda x: x['commentID']==_id, review), None)
        return reviews, 200 if reviews else 404

    @jwt_required()
    def delete(self, _id):
        global review
        review=list(filter(lambda x: x['commentID']!=_id, review))
        return {'message' : 'Review #'+_id +' deleted', 'review': review}

    @jwt_required()
    def put(self, _id):
        data = request.get_json(force=True)
        reviews = next(filter(lambda x: x['commentID']==_id, review), None)
        if reviews is None:
            reviews={'_id': _id, 'commentID': str(commentID), 'commenter': data['commenter'], 'comment': data['comment'], 'entryDate': str(dateToday)}
            reviews.append(reviews)
        else:
            reviews.update(data)
        return reviews

    @jwt_required()
    def patch(self, _id):
        data = request.get_json(force=True)
        reviews = next(filter(lambda x: x['commentID']==_id, review), None)
        if reviews is None:
            reviews={'_id': _id, 'commentID': str(commentID), 'commenter': data['commenter'], 'comment': data['comment'], 'entryDate': str(dateToday)}
            reviews.append(reviews)
        else:
            reviews.update(data)
        return reviews


# End point setup
api.add_resource(Music, '/songs/<string:_id>') # _id = song id
api.add_resource(MusicAll, '/songs')
api.add_resource(AllReview, '/reviews/<string:_id>')   # _id = comment ID

app.run(port=5000, debug=True)
