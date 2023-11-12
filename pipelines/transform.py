import tensorflow as tf
import tfx.v1 as tfx
from transformers import AutoTokenizer


MODEL_NAME = "beomi/KoAlpaca-llama-1-7b"

TEXT_FEATURES = {
    'en': None,
    'ko': None,
}

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

def preprocessing_fn(inputs):
    outputs = {}

    en = str(inputs['en'])
    ko = str(inputs['ko'])

    output_en = tokenizer(en,
                          padding=True,
                          truncation=True,
                          max_length=512,
                          return_tensors="tf",
                          )
    
    output_ko = tokenizer(ko,
                          padding=True,
                          truncation=True,
                          max_length=512,
                          return_tensors="tf",
                          )
    
    outputs['en_seq_xf'] = tf.cast(output_en['input_ids'], dtype=tf.int64)
    outputs['en_att_xf'] = tf.cast(output_en['attention_mask'], dtype=tf.int64)
    outputs['ko_seq_xf'] = tf.cast(output_ko['input_ids'], dtype=tf.int64)
    outputs['ko_att_xf'] = tf.cast(output_ko['attention_mask'], dtype=tf.int64)

    return outputs