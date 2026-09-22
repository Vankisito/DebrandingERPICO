/* © 2026 Habitat Digital */
/* License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html). */

import { OutOfFocusService } from "@mail/core/common/out_of_focus_service";
import { htmlToTextContentInline } from "@mail/utils/common/format";
import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";

const PREVIEW_MSG_MAX_SIZE = 350;

patch(OutOfFocusService.prototype, {
    async notify(message, thread) {
        const messageTypesHandledByPush = [
            "comment",
            "email",
            "notification",
            "user_notification",
            "whatsapp_message",
        ];
        if (
            messageTypesHandledByPush.includes(message.message_type) &&
            !message.isSelfAuthored &&
            (await this.hasServiceWorkInstalledAndPushSubscriptionActive())
        ) {
            return;
        }
        const author = message.author;
        let notificationTitle;
        let icon = "/erpico_debranding/static/src/img/bot_placeholder.png";
        if (!author) {
            notificationTitle = _t("New message");
        } else {
            icon = author.avatarUrl;
            if (message.thread?.channel_type === "channel") {
                notificationTitle = _t("%(author name)s from %(channel name)s", {
                    "author name": message.authorName,
                    "channel name": message.thread.displayName,
                });
            } else {
                notificationTitle = message.authorName;
            }
        }
        const notificationContent = htmlToTextContentInline(message.previewText).substring(
            0,
            PREVIEW_MSG_MAX_SIZE
        );
        await this.sendNotification({
            message: notificationContent,
            sound: message.thread?.model === "discuss.channel",
            title: notificationTitle,
            type: "info",
            icon,
        });
    },
});