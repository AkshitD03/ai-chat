from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired
import freeGPT
from freeGPT import AsyncClient
from PIL import Image
from io import BytesIO
from asyncio import run


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Sample data structure to store chatbot information
chatbots = []

# Form for creating chatbots
class ChatbotForm(FlaskForm):
    bot_name = StringField('Chatbot Name', validators=[InputRequired()])
    bot_description = TextAreaField('Description', validators=[InputRequired()])
    bot_behavior = TextAreaField('Chatbot Behavior', validators=[InputRequired()])

# Sample function to interact with the AI chatbot
async def chat_with_bot(prompt):
    try:
        # resp = await AsyncClient.create_completion("gpt4", prompt)
        
        # return resp
         resp = await AsyncClient.create_completion("gpt3", prompt)
         
         return resp
    except Exception as e:
        return str(e)

@app.route('/')
def marketplace():
    return render_template('index.html', chatbots=chatbots)

@app.route('/create', methods=['GET', 'POST'])
def create_chatbot():
    form = ChatbotForm()
    if form.validate_on_submit():
        chatbot_data = {
            'bot_name': form.bot_name.data,
            'bot_description': form.bot_description.data,
            'bot_behavior': form.bot_behavior.data,
        }
        chatbots.append(chatbot_data)
        return redirect(url_for('marketplace'))
    return render_template('create_chatbot.html', form=form)

@app.route('/chatbot/<bot_name>', methods=['GET', 'POST'])
def chatbot_view(bot_name):
    chatbot = next((bot for bot in chatbots if bot['bot_name'] == bot_name), None)
    if chatbot:
        if request.method == 'POST':
            user_input = request.form['user_input']
            prompt = chatbot['bot_behavior'] + user_input
            ai_response = run(chat_with_bot(prompt))
            return render_template('chatbot_view.html', chatbot=chatbot, user_input=user_input, ai_response=ai_response)
        return render_template('chatbot_view.html', chatbot=chatbot)
    return 'Chatbot not found', 404

# AI interaction route
@app.route('/chatbot_interaction', methods=['POST'])
def chatbot_interaction():
    try:
        data = request.get_json()
        prompt = data['prompt']

        # Combine prompt and user input (you can add user input here)
        combined_input = prompt

        # Use the AI model to generate a response
        ai_response = run(chat_with_bot(combined_input))

        return jsonify({'response': ai_response})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete_chatbot/<bot_name>', methods=['POST'])
def delete_chatbot(bot_name):
    global chatbots  # Access the global chatbots list
    chatbots = [bot for bot in chatbots if bot['bot_name'] != bot_name]
    return redirect(url_for('marketplace'))
@app.route('/app2_action')
def app2_action():
    # Perform some action in the second app
    return "Action in App 2"

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
