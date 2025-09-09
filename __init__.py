# GNU GENERAL PUBLIC LICENSE
#    Version 3, 29 June 2007
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# TODO
# Improve error handling
# support additional notifications
# add test button if possible

from pynicotine.pluginsystem import BasePlugin
import requests

class Plugin(BasePlugin):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.settings = {
            "webhookurl": "",
            "botname": "Nicotine+",
            "avatarurl": "https://raw.githubusercontent.com/nicotine-plus/nicotine-plus/refs/heads/master/pynicotine/gtkgui/icons/hicolor/256x256/apps/org.nicotine_plus.Nicotine.png",
            "enable-priv-messages": True,
            "enable-room-messages": False,
        }

        self.metasettings = {
            "webhookurl": {
                "description": "Webhook URL",
                "type": "string"
            },
            "botname": {
                "description": "Webhook Name",
                "type": "string"
            },
            "avatarurl": {
                "description": "Avatar URL",
                "type": "string"
            },
            "enable-priv-messages": {
                "description": "Forward Private Messages",
                "type": "bool"
            },
            "enable-room-messages": {
                "description": "Forward Chatroom Messages",
                "type": "bool"
            }
        }

    def webhooksend(self, text_content, embed):
        payload = {
            "username": self.settings["botname"],
            "avatar_url": self.settings["avatarurl"],
            "embeds": [embed],
            "content": text_content
        }

        payload["embeds"][0]["color"] = int(payload["embeds"][0]["color"], 16)
        payload["embeds"][0]["description"] = payload["embeds"][0]["description"][:4096]

        requests.post(self.settings["webhookurl"], json=payload)

    def incoming_private_chat_notification(self, user, line):
        if self.settings["enable-priv-messages"]:
            embed = {
                "description": line,
                "author": {
                    "name": user
                },
                "color": "FFA0FF"
            }

            self.webhooksend("New Private Message", embed)

    def incoming_public_chat_notification(self, room, user, line):
        if self.settings["enable-room-messages"]:
            embed = {
                "description": line,
                "author": {
                    "name": user
                },
                "color": "FFA000"
            }

            self.webhooksend("New Chatroom Message", embed)