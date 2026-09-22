# © 2026 Habitat Digital
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from markupsafe import Markup

from odoo import models


class MailBot(models.AbstractModel):
    _inherit = 'mail.bot'

    @staticmethod
    def _get_style_dict():
        return {
            'new_line': Markup('<br>'),
            'bold_start': Markup('<b>'),
            'bold_end': Markup('</b>'),
            'command_start': Markup("<span class='o_odoobot_command'>"),
            'command_end': Markup('</span>'),
            'document_link_start': Markup(''),
            'document_link_end': Markup(''),
            'slides_link_start': Markup(''),
            'slides_link_end': Markup(''),
            'paperclip_icon': Markup("<i class='fa fa-paperclip' aria-hidden='true'/>"),
        }

    def _get_answer(self, channel, body, values, command=False):
        answer = super()._get_answer(channel, body, values, command=command)
        if not answer:
            return answer
        answers = answer if isinstance(answer, list) else [answer]
        neutral = []
        for ans in answers:
            for source, target in (
                ('@OdooBot', '@ERPICO Assistant'),
                ('Enjoy exploring Odoo!', 'Enjoy exploring ERPICO!'),
            ):
                if isinstance(ans, Markup):
                    ans = Markup(str(ans).replace(source, target))
                else:
                    ans = ans.replace(source, target)
            neutral.append(ans)
        return neutral if isinstance(answer, list) else neutral[0]