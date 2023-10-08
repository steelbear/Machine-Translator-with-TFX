import os
import json
from typing import Dict, Any

from absl import logging
import apache_beam as beam
import tensorflow as tf

from tfx.components.example_gen.base_example_gen_executor import BaseExampleGenExecutor
from tfx.types import standard_component_specs


@beam.typehints.with_input_types(Dict[str, Any])
@beam.typehints.with_output_types(tf.train.Example)
def _DictToExample(record_dict: Dict[str, Any]) -> tf.train.Example:
    def bytes_feature(value):
        if isinstance(value, type(tf.constant(0))):
            value = value.numpy()
        return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))
    
    ko_bytes = bytes(record_dict['ko'].encode('utf-8'))
    en_bytes = bytes(record_dict['en'].encode('utf-8'))
    ko_string = bytes_feature(ko_bytes)
    en_string = bytes_feature(en_bytes)

    return tf.train.Example(features=tf.train.Features(feature={
        'ko': ko_string,
        'en': en_string,
    }))


@beam.ptransform_fn
@beam.typehints.with_input_types(beam.Pipeline)
@beam.typehints.with_output_types(tf.train.Example)
def _JsonToExample(
    pipeline: beam.Pipeline, exec_properties: Dict[str, Any], split_pattern: str) -> beam.pvalue.PCollection:
    """
    """
    input_base_uri = exec_properties[standard_component_specs.INPUT_BASE_KEY]
    json_pattern = os.path.join(input_base_uri, split_pattern)
    logging.info('Processing input json data %s to TFExample', json_pattern)

    return (pipeline
            | 'ReadFromTextFile' >> beam.io.ReadFromText(json_pattern)
            | 'ConvertToJson' >> beam.Map(json.loads)
            | 'ToTFExample' >> beam.Map(_DictToExample)
            #| 'print' >> beam.ParDo(print)
    )


class Executor(BaseExampleGenExecutor):
    def GetInputSourceToExamplePTransform(self) -> beam.PTransform:
        return _JsonToExample