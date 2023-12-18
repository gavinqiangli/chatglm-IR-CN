from dotenv import load_dotenv
import os
import zhipuai
import streamlit as st
from streamlit_chat import message

# your api key
load_dotenv()
zhipuai.api_key = os.getenv("ZHIPUAI_API_KEY")

def invoke_example(user_input):
    response = zhipuai.model_api.invoke(
        model="chatglm_turbo",
        prompt=[{"role": "user", "content": user_input}],
        top_p=0.7,
        temperature=0.9,
    )
    print(response)
    return response

def async_invoke_example():
    response = zhipuai.model_api.async_invoke(
        model="chatglm_turbo",
        prompt=[{"role": "user", "content": "人工智能"}],
        top_p=0.7,
        temperature=0.9,
    )
    print(response)

def sse_invoke_example():
    response = zhipuai.model_api.sse_invoke(
        model="chatglm_turbo",
        prompt=[{"role": "user", "content": "人工智能"}],
        top_p=0.7,
        temperature=0.9,
    )

    for event in response.events():
        if event.event == "add":
            print(event.data)
        elif event.event == "error" or event.event == "interrupted":
            print(event.data)
        elif event.event == "finish":
            print(event.data)
            print(event.meta)
        else:
            print(event.data)
        

def query_async_invoke_result_example():
    response = zhipuai.model_api.query_async_invoke_result("your task_id")
    print(response)


# invoke_example("中国电信2023年前三季度业绩?")
# print(" 中国电信2023年前三季度业绩如下：\n\n1. 营业收入：中国电信在前三季度实现了营业收入3811.03亿元，同比增长6.5%。其中，服务收入为3497.43亿元，同比增长6.4%。\n\n2. 净利润：2023年前三季度，中国电信归属于上市公司股东的净利润为271.01亿元，同比增长10.4%。归属于上市公司股东的扣除非经常性损益的净利润为272.12亿元，同比增长10.7%。\n\n3. 移动通信服务：中国电信不断优化5G网络覆盖，加快5G应用AI智能化升级。2023年前三季度，移动通信服务收入为1519.16亿元，同比增长2.4%。移动用户净增1463万户，达到约4.06亿户。5G套餐用户净增3965万户，达到约3.08亿户，渗透率达到75.8%。\n\n4. 业务发展：中国电信加强了数字化转型，深化了各项战略性新兴业务的布局。在前三季度，公司各项业务得到了持续优化，客户需求得到了有效满足。\n\n总体来说，中国电信在2023年前三季度取得了良好的业绩，营业收入和净利润均实现了增长。公司在移动通信服务方面取得了显著成果，5G网络覆盖和套餐用户数持续增长。同时，中国电信加速了数字化转型，提升了各项业务的竞争力。")

# Use streamlit to create a web app

def on_input_change():
    user_input = st.session_state.user_input
    st.session_state.past.append(user_input)

    # Generate AI response using user input (replace this with your AI model)
    response = invoke_example(user_input)
    # Extracting the 'content' part from response json
    ai_response = response.get('data', {}).get('choices', [])[0].get('content', '')
    # Replace '\\n' with actual new lines
    ai_response = ai_response.replace('\\n', '\n')
    # ai_response = " 中国电信2023年前三季度业绩如下：\n\n1. 营业收入：中国电信在前三季度实现了营业收入3811.03亿元，同比增长6.5%。其中，服务收入为3497.43亿元，同比增长6.4%。\n\n2. 净利润：2023年前三季度，中国电信归属于上市公司股东的净利润为271.01亿元，同比增长10.4%。归属于上市公司股东的扣除非经常性损益的净利润为272.12亿元，同比增长10.7%。\n\n3. 移动通信服务：中国电信不断优化5G网络覆盖，加快5G应用AI智能化升级。2023年前三季度，移动通信服务收入为1519.16亿元，同比增长2.4%。移动用户净增1463万户，达到约4.06亿户。5G套餐用户净增3965万户，达到约3.08亿户，渗透率达到75.8%。\n\n4. 业务发展：中国电信加强了数字化转型，深化了各项战略性新兴业务的布局。在前三季度，公司各项业务得到了持续优化，客户需求得到了有效满足。\n\n总体来说，中国电信在2023年前三季度取得了良好的业绩，营业收入和净利润均实现了增长。公司在移动通信服务方面取得了显著成果，5G网络覆盖和套餐用户数持续增长。同时，中国电信加速了数字化转型，提升了各项业务的竞争力。"
    print(ai_response)
    
    st.session_state.generated.append(ai_response)

    # Display the AI response
    message(user_input, is_user=True, key=f"{len(st.session_state.past)-1}_user")
    message(ai_response, key=f"{len(st.session_state.generated)-1}_{ai_response}")


def on_btn_click():
    st.session_state.past.clear()
    st.session_state.generated.clear()


st.session_state.setdefault('past', [])
st.session_state.setdefault('generated', [])

# Use streamlit to create a web app
st.set_page_config(page_title="智能IR助手", page_icon=":bird:")

# this markdown is for hiding "github" button
st.markdown("<style>#MainMenu{visibility:hidden;}</style>", unsafe_allow_html=True)
st.markdown("<style>footer{visibility: hidden;}</style>", unsafe_allow_html=True)
st.markdown("<style>header{visibility: hidden;}</style>", unsafe_allow_html=True)
st.markdown(
    """
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob, .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137, .viewerBadge_text__1JaDK{display: none;} 
    </style>
    """,
    unsafe_allow_html=True
    )

st.header("智能IR助手 :bird:")

chat_placeholder = st.empty()

with chat_placeholder.container():    
    for i in range(len(st.session_state['generated'])):                
        message(st.session_state['past'][i], is_user=True, key=f"{i}_user_{st.session_state['past'][i]}")
        message(st.session_state['generated'][i], key=f"{i}")
    
    st.button("清除聊天记录", on_click=on_btn_click)


with st.container():
    st.text_input("请输入您的问题.例如:中国电信2023年前三季度业绩?", on_change=on_input_change, key="user_input")