import os

from absl import logging
import tfx.v1 as tfx
from tfx.components import StatisticsGen, SchemaGen, Transform
from tfx.components.example_gen.component import FileBasedExampleGen
from tfx.dsl.components.base import executor_spec

from custom_executor.json_executor import Executor as JsonExecutor

PIPELINE_NAME = 'machine-translator'

PIPELINE_ROOT = os.path.join('pilelines', PIPELINE_NAME)
METADATA_PATH = os.path.join('metadata', PIPELINE_NAME, 'metadata.db')

DATA_ROOT = os.path.join('data', 'train')

logging.set_verbosity(logging.INFO)


def create_pipeline(pipeline_name: str, pipeline_root: str, data_root: str, metadata_path: str) -> tfx.dsl.Pipeline:
    example_gen = FileBasedExampleGen(
        input_base=data_root,
        custom_executor_spec=executor_spec.BeamExecutorSpec(JsonExecutor)
    )
    
    statistics_gen = StatisticsGen(
        examples=example_gen.outputs['examples']
    )

    schema_gen = SchemaGen(
        statistics=statistics_gen.outputs['statistics']
    )

    transform = Transform(
        examples=example_gen.outputs['examples'],
        schema=schema_gen.outputs['schema'],
        module_file=os.path.abspath('pipelines/transform.py'),
    )


    components = [
        example_gen,
        statistics_gen,
        schema_gen,
        transform,
    ]

    return tfx.dsl.Pipeline(
        pipeline_name=pipeline_name,
        pileline_root=pipeline_root,
        metadata_connection_config=tfx.orchestration.metadata.sqlite_metadata_connection_config(metadata_path),
        components=components,
    )

tfx.orchestration.LocalDagRunner().run(
    create_pipeline(
        pipeline_name=PIPELINE_NAME,
        pipeline_root=PIPELINE_ROOT,
        data_root=DATA_ROOT,
        metadata_path=METADATA_PATH,
    )
)