var vm = new Vue({
	el: '#app',
	data: {
		error_name: false,
		error_password: false,
		error_check_password: false,
		error_phone: false,
		error_allow: false,
		error_image_code: false,
		error_sms_code: false,

		username: '',
		password: '',
		password2: '',
		mobile: '', 
		image_code: '',
		sms_code: '',
		allow: false,
		error_name_message: '请输入5-20个字符的用户',
		error_phone_message: '您输入的手机号格式不正确',
	},
	methods: {
		   check_username: function (){
            var len = this.username.length;
            if(len<5||len>20) {
                this.error_name = true;
            } else {
                this.error_name_message = '请输入5-20个字符的用户名';
                this.error_name = false;
            }
            // 检查重名
            if (this.error_name == false){
                axios.get('http://127.0.0.1:8000'+'/users/usernames/' + this.username + '/count/', {
                        responseType: 'json'
                    })
                    .then(response => {
                        if (response.data.count > 0) {
                            this.error_name_message = '用户名已存在';
                            this.error_name = true;
                        } else {
                            this.error_name = false;
                        }
                    })
                    .catch(error => {
                        console.log(error.response.data);
                    })
            }
        },
		   check_phone: function (){
            var re = /^1[345789]\d{9}$/;
            if(re.test(this.mobile)) {
                this.error_phone = false;
            } else {
                this.error_phone_message = '您输入的手机号格式不正确';
                this.error_phone = true;
            }
            if (this.error_phone == false) {
                axios.get('http://127.0.0.1:8000'+'/users/phones/'+ this.mobile + '/count/', {
                        responseType: 'json'
                    })
                    .then(response => {
                        if (response.data.count > 0) {
                            this.error_phone_message = '手机号已存在';
                            this.error_phone = true;
                        } else {
                            this.error_phone = false;
                        }
                    })
                    .catch(error => {
                        console.log(error.response.data);
                    })
            }
        },
		check_image_code: function (){
			if(!this.image_code) {
				this.error_image_code = true;
			} else {
				this.error_image_code = false;
			}	
		},
		check_sms_code: function(){
			if(!this.sms_code){
				this.error_sms_code = true;
			} else {
				this.error_sms_code = false;
			}
		},
		check_allow: function(){
			if(!this.allow) {
				this.error_allow = true;
			} else {
				this.error_allow = false;
			}
		},
		// 注册
		on_submit: function(){
			this.check_username();
			this.check_pwd();
			this.check_cpwd();
			this.check_phone();
			this.check_sms_code();
			this.check_allow();
		}
	}
});
