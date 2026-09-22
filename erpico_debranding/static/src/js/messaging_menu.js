/* © 2026 Habitat Digital */
/* License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html). */

import { MessagingMenu } from "@mail/core/public_web/messaging_menu";
import { patch } from "@web/core/utils/patch";

patch(MessagingMenu.prototype, {
    get canPromptToInstall() {
        return false;
    },
});