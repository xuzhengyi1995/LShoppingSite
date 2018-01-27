# LoginHandler
# XUZhengyi, 26/01/2018

import tornado.web
import json
from handlers.BasicHandler import BasicHandler
from common.CheckreCAPTCHA import check_reCAPTCHA


class LoginHandler(BasicHandler):
    def get(self):
        self.info['title'] = '登录'
        self.info['cat'] = ['Login']
        self.render('login.html', info=self.info)

    def post(self):
        email = self.get_argument('email')
        pas = self.get_argument('password')
        gl = self.get_argument('g-recaptcha-response')

        self.set_header("Content-Type", 'application/json')
        if(not check_reCAPTCHA(gl)):
            self.write(json.dumps({'is_error': True, 'error_info': '请进行人机身份验证！'}))
            self.finish()
            return

        #TODO:Check the user from database
        self.write(json.dumps({'is_error': True, 'error_info': '验证码测试通过！'}))
