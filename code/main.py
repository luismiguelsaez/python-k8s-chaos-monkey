from kubernetes import client, config
from os import environ
from sys import exit
from time import sleep
from random import randrange
from prometheus_client import Counter, start_http_server

def main():

    # Initialize prometheus metrics
    prom_count_killed = Counter('container_killed', 'Killed containers count')

    start_http_server(8080)

    # Create config object from internal mounted credentials
    try:
      config.load_incluster_config()
    except config.config_exception.ConfigException as k_exc:
      print("Kubernetes API not reachable! Exiting application ...")
      exit(1)

    # Check mandatory environment variables
    for param in ["CM_NAMESPACE","CM_INTERVAL","CM_LABELS"]:
      if param not in environ:
        print("Required environment variable [%s] not set! Exiting ..." % ( param ) )
        exit(1)

    namespace = environ['CM_NAMESPACE']
    interval  = environ['CM_INTERVAL']
    labels = environ['CM_LABELS']

    print("Getting pods from namespace [%s]" % ( namespace ) )

    v1 = client.CoreV1Api()

    # Start application main loop
    while True:
      try:
        # Get pods in the selected namespace
        pod_list = v1.list_namespaced_pod(namespace=namespace,label_selector=labels)
      except client.exceptions.ApiException as p_exec:
        print("Insuficient permissions while trying to get pods from namespace [%s]! Exiting ..." % ( namespace ) )
        exit(1)

      # Iterate over items, filtering by status phase
      c = 0
      pod_running_list = []
      for pod in pod_list.items:
        if pod.status.phase == 'Running':
          c += 1
          pod_running_list.append(pod.metadata.name)

      print("Got [%s] pods from resource of type [%s]" % ( str(c), pod_list.kind ) )

      if c > 0:
        # Select random index number
        pod_item_number = randrange(1,c+1)
        print("Going to kill pod number [%s] of [%s]" % ( str(pod_item_number), str(c) ) )
        # Delete selected pod by name
        try:
          v1.delete_namespaced_pod(pod_running_list[pod_item_number-1], namespace)
        except Exception as d_exc:
          print("Not able to delete pod due to exception: %s" % ( d_exc.message ) )
        # Increment killed containers prometheus metric
        prom_count_killed.inc(1)
      else:
        print("Skipping, as no pods were found in namespace [%s]" % ( namespace ) )

      # Sleep for the configured interval seconds
      print("Sleeping for [%s] seconds ..." % ( interval ) )
      sleep(int(interval))


if __name__ == '__main__':
    main()
