import apache_beam as beam
import argparse
import sys
import time

from apache_beam.utils.options import PipelineOptions
from subprocess import PIPE, Popen

def run_pipeline(args):
  p = beam.Pipeline(
          options=PipelineOptions(
          job_name='policyscanner',
          runner=args['runner_type'],
          project=args['project_id'],
          staging_location='{}/staging'.format(args['gcs_prefix']),
          temp_location='{}/tmp'.format(args['gcs_prefix']),
        ))

  (p
   | 'add names' >> beam.Create(['Alice', 'Bob', 'Eve'])
   | 'save' >> beam.io.Write(beam.io.textio.WriteToText(args['output']))
  )

  p.run()

if __name__ == '__main__':
  ap = argparse.ArgumentParser()
  ap.add_argument('--project', help='Project Id')
  ap.add_argument('--runner_type', help='Dataflow Runner')
  args = ap.parse_args()

  if args.project:
    project_id = args.project
  else:
    process = Popen(['gcloud', 'beta', 'config', 'get-value',
                     'core/project'],
                     stdout=PIPE, stderr=PIPE)
    out, err = process.communicate()
    lines = out.split('\n')
    project_id = lines[0].strip()

  if not project_id:
    print 'Invalid project id from output {}'.format(out)
    sys.exit(1)

  if args.runner_type:
    runner_type = args.runner_type
  else:
    runner_type = 'DataflowPipelineRunner'

  current_time = time.strftime('%Y%m%d_%H%M%S', time.gmtime())
  gcs_prefix = 'gs://{}.appspot.com'.format(project_id)
  args = {
    'project_id': project_id,
    'runner_type': runner_type,
    'gcs_prefix': gcs_prefix,
    'output': '{}/junk/out-{}'.format(gcs_prefix, current_time)
  }
  print 'Running pipeline with args {}'.format(args)
  run_pipeline(args)
