from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import requests, json


import errno
import os
import sys, random
import tempfile

import bs4
from bs4 import BeautifulSoup

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent,
)

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('change to your channel access token')
# Channel Secret
handler = WebhookHandler('change to your channel secret')
#===========[ NOTE SAVER ]=======================
notes = {}
#================================================
#index web
@app.route("/", methods=['GET'])
def index(): 
    indexs = ('Hello World!')
    return indexs

# Post Request
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text #simplify for receove message
    sender = event.source.user_id #get user_id
    gid = event.source.sender_id #get group_id
#=====[ LEAVE GROUP OR ROOM ]==========
    if text == 'bye':
        if isinstance(event.source, SourceGroup):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='Leaving group'))
            line_bot_api.leave_group(event.source.group_id)
        elif isinstance(event.source, SourceRoom):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='Leaving group'))
            line_bot_api.leave_room(event.source.room_id)
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Bot can't leave from 1:1 chat"))
#=====[ TEMPLATE MESSAGE ]=============
    elif text == '/template':
        buttons_template = TemplateSendMessage(
            alt_text='template',
            template=ButtonsTemplate(
                title='[ TEMPLATE MSG ]',
                text= 'Tap the Button',
                actions=[
                    MessageTemplateAction(
                        label='kolom 1',
                        text='/renbot'
                    ),
                    MessageTemplateAction(
                        label='kolom 2',
                        text='/renbot'
                    ),
                    MessageTemplateAction(
                        label='kolom 3',
                        text='/renbot'
                    )
                ]
            )
        )
        
        line_bot_api.reply_message(event.reply_token, buttons_template)
#=====[ CAROUSEL MESSAGE ]==========
    elif text == 'help':
        message = TemplateSendMessage(
            alt_text='OTHER MENU',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        title='Keyword',
                        text='Toram Online',
                        actions=[
                            #MessageTemplateAction(
                            #    label='Toram News',
                            #    text='toramnews'
                            #),
                            PostbackTemplateAction(
                                label='Skill Simulator',
                                text='skillsimulator',
                                data='action=buy&itemid=1'
                            ),
                            MessageTemplateAction(
                                label='StatFormula',
                                text='statformula'
                            )
                        ]
                    ),
                    CarouselColumn(
                        title='keyword 2',
                        text='Media',
                        actions=[
                            URITemplateAction(
                                label='lorem',
                                uri='https://google.com'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
#=====[ FLEX MESSAGE ]==========
    elif text == 'flex':
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://lh5.googleusercontent.com/VoOmR6tVRwKEow0HySsJ_UdrQrqrpwUwSzQnGa0yBeqSex-4Osar2w-JohT6yPu4Vl4qchND78aU2c5a5Bhl=w1366-h641-rw',
                size='full',
                aspect_ratio='20:13',
                aspect_mode='cover',
                action=URIAction(uri='http://line.me/ti/p/~tiodarren', label='label')
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    # title
                    TextComponent(text='renbot', weight='bold', size='xl'),
                    # review
                    BoxComponent(
                        layout='baseline',
                        margin='md',
                        contents=[
                            IconComponent(size='sm', url='https://example.com/gold_star.png'),
                            IconComponent(size='sm', url='https://example.com/grey_star.png'),
                            IconComponent(size='sm', url='https://example.com/gold_star.png'),
                            IconComponent(size='sm', url='https://example.com/gold_star.png'),
                            IconComponent(size='sm', url='https://example.com/grey_star.png'),
                            TextComponent(text='4.0', size='sm', color='#999999', margin='md',
                                          flex=0)
                        ]
                    ),
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Place',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text='Tangerang, Indonesia',
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Time',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text="10:00 - 23:00",
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    # separator
                    SeparatorComponent(),
                    # websiteAction
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='renbot', uri="https://line.me/ti/p/~tiodarren")
                    )
                ]
            ),
        )
        message = FlexSendMessage(alt_text="hello", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
        
#=====[ FLEX MESSAGE ]==========
    elif text == 'flexs':
        bubble = BubbleContainer(
            direction='ltr',
            #hero=ImageComponent(
            #    url='https://lh5.googleusercontent.com/VoOmR6tVRwKEow0HySsJ_UdrQrqrpwUwSzQnGa0yBeqSex-4Osar2w-JohT6yPu4Vl4qchND78aU2c5a5Bhl=w1366-h641-rw',
            #    size='full',
            #    aspect_ratio='20:13',
            #    aspect_mode='cover',
            #    action=URIAction(uri='http://line.me/ti/p/~tiodarren', label='label')
            #),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    # title
                    TextComponent(text='Berita Terbaru ToramOnline', weight='bold', size='xs'),
                    # review
                    #BoxComponent(
                    #    layout='baseline',
                    #    margin='md',
                    #    contents=[
                    #        IconComponent(size='sm', url='https://ubisafe.org/images/orange-transparent-stars-3.gif'),
                    #        IconComponent(size='sm', url='https://ubisafe.org/images/orange-transparent-stars-3.gif'),
                    #        IconComponent(size='sm', url='https://ubisafe.org/images/orange-transparent-stars-3.gif'),
                    #        IconComponent(size='sm', url='https://ubisafe.org/images/orange-transparent-stars-3.gif'),
                    #        IconComponent(size='sm', url='http://www.clker.com/cliparts/2/4/T/f/0/4/star-grey-hi.png'),
                    #        TextComponent(text='4.0', size='sm', color='#999999', margin='md',
                    #                      flex=0)
                    #    ]
                    #),
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Time:',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text='Ini Jam',
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Title:',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text="Judul.................................................",
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    # separator
                    SeparatorComponent(),
                    # websiteAction
                    ButtonComponent(
                        color='#1DB446',
                        style='link',
                        height='sm',
                        action=URIAction(uri="http://id.toram.jp/information/?type_code=all",label='See More...')
                    )
                ]
            ),
        )
        message = FlexSendMessage(alt_text="hello", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
        
    if text == 'toramnews':
    #============TESTING======================
        source = requests.get('http://id.toram.jp/information/?type_code=all/')
        bsoup = BeautifulSoup(source.text, 'html5lib')
        dataraw = bsoup.find('div',{'class':'useBox'}) #find tag <div class=> in source
        dataa = dataraw.find_all('li') #find all tags<li> in dataraw <div>
        i = 0
        hasil = "「Berita Terbaru ToramOnline」\n"
        for final in dataa :
            while i <=8 :
                data = dataa[i].find('a')
                #time = data.find('time').text
                link = data.get('href')
                title3 = data.text
                title2 = title3.replace("2018-","Time: 2018-")
                title = title2.replace("								","\nTitle: ")
                #titles = title.replace("								","")
                #titletime = time +' '+ title #time title
                links = "http://id.toram.jp"+link #http://id.toram.jp/link
                #===================================================#
                web = requests.get("https://tinyurl.com/create.php?source=indexpage&url="+ links)
                shorturl = BeautifulSoup(web.text, 'html5lib')
                short  = shorturl.find_all('div',class_='indent')
                short = short[1].find('b').text
                #====================================================#
                hasil += "\n"+title+"\nLink: "+short
                i=i+1
            else :
               pass
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=hasil + "\n\nSelengkapnya Lihat Disini" "\nhttp://id.toram.jp/information/?type_code=all"))

    #=========================================
    """
            bubble = BubbleContainer(
            direction='ltr',
            body=BoxComponent(
                layout='vertical',
                contents=[
                    # title
                    TextComponent(text='Berita Terbaru ToramOnline', weight='bold', size='xs'),
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            #BoxComponent(
                            #    layout='baseline',
                            #    spacing='sm',
                            #    contents=[
                            #       TextComponent(
                            #            text='Time:',
                            #            color='#aaaaaa',
                            #           size='sm',
                            #            flex=1
                            #        ),
                            #        TextComponent(
                            #            text='Ini Jam',
                            #            wrap=True,
                            #            color='#666666',
                            #            size='sm',
                            #            flex=5
                            #        )
                            #    ],
                            #),
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Title:',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text=titles,
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                    ),
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Link:',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text=short,
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    # separator
                    SeparatorComponent(),
                    # websiteAction
                    ButtonComponent(
                        color='#1DB446',
                        style='link',
                        height='sm',
                        action=URIAction(uri="http://id.toram.jp/information/?type_code=all",label='See More...')
                    )
                ]
            ),
        )
        message = FlexSendMessage(alt_text="hello", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
    """
        
        
        
#=======================================================================================================================
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
