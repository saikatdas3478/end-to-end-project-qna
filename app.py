import streamlit as st
import tensorflow as tf
from transformers import AutoTokenizer, TFAutoModelForQuestionAnswering

# Loading the pre-trained model

loaded_model = TFAutoModelForQuestionAnswering.from_pretrained('Question_Answer_system_transformer')

# Loading the tokenizer

loaded_tokenizer = AutoTokenizer.from_pretrained('qna_modified_tokenizer')
    

# Getting answer from the questions and context

def answer_generator(context, question, model = loaded_model, tokenizer = loaded_tokenizer):
    
    input_seq = tokenizer([context], [question], return_tensors = 'np')
    
    output_seq = model(input_seq)
    
    answer_start = tf.argmax(output_seq.start_logits, axis = 1)
    answer_end = tf.argmax(output_seq.end_logits, axis = 1)
    
    answer_seq = input_seq['input_ids'][0, int(answer_start):int(answer_end) + 1]
    
    answer_text = tokenizer.decode(answer_seq).strip()
    
    return answer_text
        
        
# Interface       

st.write('### QnA Helper')
st.subheader('')
context = st.text_area(label = '**Context..** (***Required***)',
                        max_chars= 2000,
                        height = 200,
                        placeholder = 'Context here...')


questions = [st.text_input(label = f'Enter the Question {i + 1}', placeholder = 'Question here..') for i in range(3)]

if st.button(label = 'Reset'):
    context = ['']
    
    questions = ['', '', '']
    

if st.button(label = 'Get Answers'):
    
    if context:
        
        if any(questions):
            
            for i, question in enumerate(questions):
                
                if question:
                    
                    st.write(f'Question {i+1}: {question}')
                    answer = answer_generator(context, question)
                    st.write(f'Answer: {answer}')
        else:
            st.warning('Please enter atleast one question')
            
    else:
        st.warning('Please enter the context')


    