from flask import url_for
from flask_testing import TestCase

import thermos
from ..models import User, Bookmark


class ThermosTestCase(TestCase):

    def create_app(self):
        return thermos.create_app('test')

    def setUp(self):
        self.db = thermos.db
        self.db.create_all()
        self.client = self.app.test_client()

        u = User(username='testuser1', email='testuser1@email.com', password='testuser1')
        bm = Bookmark(user=u, url='https://google.com', tags='t1,t2')

        self.db.session.add(u)
        self.db.session.add(bm)
        self.db.session.commit()

        self.client.post(
            url_for('auth.login'),
            data=dict(username='testuser1', password='testuser1')
        )

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

    def test_delete_all_tags(self):
        response = self.client.post(
            url_for('bookmark.edit_bookmark', bookmark_id=1),
            data=dict(
                url='http://testurl.com',
                tags=''
            ),
            follow_redirects=True
        )
        assert response.status_code == 200
        bm = Bookmark.query.first()
        assert not bm._tags
