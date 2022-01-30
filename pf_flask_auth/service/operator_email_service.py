from pf_flask_auth.common.pffa_auth_message import PFFAuthMessage
from pf_flask_auth.model.operator import Operator

from pf_flask_auth.common.pffa_auth_config import PFFAuthConfig
from pf_flask_mail.pffm_send_mail import PFFMSendMail
from pf_py_jinja.pfpyj_template_man import TemplateManager


class OperatorEmailService:
    _template_manager: TemplateManager = TemplateManager()

    def sent_email(self, recipient, subject, html_body):
        if PFFAuthConfig.emailConfig:
            send_email_service = PFFMSendMail(PFFAuthConfig.emailConfig)
            send_email_service.compose(recipient, subject)
            send_email_service.add_html_message(html_body)
            send_email_service.send(use_thread=True)

    def forgot_password_email(self, token, operator: Operator, is_api: bool = False):
        url = PFFAuthConfig.emailFormAppBaseURL + PFFAuthConfig.formUrlPrefix
        if is_api:
            url = PFFAuthConfig.emailRestAppBaseURL
        url += PFFAuthConfig.resetPasswordURL + "/" + token
        html_body = self.get_html_body("auth/forgot-password.html", data={"url": url, "operator": operator})
        self.sent_email(operator.email, PFFAuthMessage.PASS_RESET_REQUEST, html_body)

    def get_html_body(self, template, data):
        self.load_template_path()
        return self._template_manager.resolve(template, data=data)

    def load_template_path(self):
        path = PFFAuthConfig.emailTemplatePath
        if path:
            self._template_manager.init_env(path)
