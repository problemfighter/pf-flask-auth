from pf_flask_auth.common.pffa_auth_message import PFFAuthMessage
from pf_flask_auth.model.operator import Operator

from pf_flask_auth.common.pffa_auth_config import PFFAuthConfig
from pf_flask_mail.pffm_send_mail import PFFMSendMail


class OperatorEmailService:

    def sent_email(self, recipient, subject, html_body):
        if PFFAuthConfig.emailConfig:
            send_email_service = PFFMSendMail(PFFAuthConfig.emailConfig)
            send_email_service.compose(recipient, subject)
            send_email_service.add_html_message(html_body)
            send_email_service.send()

    def forgot_password_email(self, token, operator: Operator, is_api: bool = False):
        url = PFFAuthConfig.emailFormAppBaseURL + PFFAuthConfig.formUrlPrefix
        if is_api:
            url = PFFAuthConfig.emailRestAppBaseURL
        url += PFFAuthConfig.resetPasswordURL + "/" + token
        self.sent_email(operator.email, PFFAuthMessage.PASS_RESET_REQUEST, url)
