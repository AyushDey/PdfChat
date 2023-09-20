css = '''
<style>
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
    }

    .chat-message.user {
        background-color: #2b313e;
        flex-direction: row-reverse; /* Reverse the order of flex items */
        justify-content: flex-start;
    }

    .chat-message.bot {
        background-color: #475063;
        flex-direction: row;
        justify-content: flex-start;
    }

    .chat-message .avatar img {
        max-width: 78px;
        max-height: 78px;
        border-radius: 50%;
        object-fit: cover;
        
    }

    .chat-message .message {
        width: 80%;
        padding: 0 1.5rem;
        color: #fff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    p {
        font-size: smaller;
        text-align: center;
        color: orange;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .chat-message.user p {
        color: yellow;
    }
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/GpN78gr/IMG-1514-2.jpg"><br>
        <p>Ayush</p>
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/6Wjg8nS/1686157004764-Original.jpg"><br>
        <p>Dayita</p>
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''
