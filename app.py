from flask import Flask, request, jsonify, render_template
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from threading import Thread
from time import sleep

app = Flask(__name__)

# Global variables for the model and tokenizer
model = None
tokenizer = None

# Function to load the model
def load_model():
    global model, tokenizer
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    model = GPT2LMHeadModel.from_pretrained('gpt2')

    # Explicitly add a padding token as GPT-2 does not have one by default
    tokenizer.pad_token = tokenizer.eos_token

# Loading the model in a separate thread
Thread(target=load_model).start()

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    input_text = data['input_text']

    # If the model is not loaded yet, wait and try again
    if model is None or tokenizer is None:
        sleep(1)
        return generate()

    # Encode the input text and also return attention mask
    inputs = tokenizer.encode_plus(input_text, return_tensors='pt', padding='longest', truncation=True, max_length=512)

    # Generate output with temperature control, top-k and top-p
    outputs = model.generate(inputs['input_ids'], 
                             attention_mask=inputs['attention_mask'], 
                             max_length=150, 
                             num_return_sequences=1, 
                             no_repeat_ngram_size=2, 
                             temperature=0.8, 
                             do_sample=True, 
                             top_k=50, 
                             top_p=0.95)

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return jsonify({'output_text': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5051)
