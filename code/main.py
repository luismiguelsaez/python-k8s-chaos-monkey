from kubernetes import client, config
from os import environ
from sys import exit
from time import sleep
from random import randrange

def main():

    try:
      config.load_incluster_config()
    except config.config_exception.ConfigException as k_exc:
      print("Kubernetes API not reachable! Exiting application ...")
      exit(1)

    for param in ["CM_NAMESPACE","CM_INTERVAL"]:
      if param not in environ:
        print("Required environment variable [%s] not set! Exiting ..." % ( param ) )
        exit(1)

    namespace = environ['CM_NAMESPACE']
    interval  = environ['CM_INTERVAL']

    print("Getting pods from namespace [%s]" % ( namespace ) )

    v1 = client.CoreV1Api()

    while True:
      try:
        pod_list = v1.list_namespaced_pod(namespace=namespace)
      except client.exceptions.ApiException as p_exec:
        print("Insuficient permissions while trying to get pods from namespace [%s]! Exiting ..." % ( namespace ) )
        exit(1)

      c = 0
      for pod in pod_list.items:
        c += 1
        #print("%s\t%s\t%s" % (pod.metadata.name, pod.status.phase, pod.status.pod_ip))

      print("Got [%s] pods from resource of type [%s]" % ( str(c), pod_list.kind ) )

      if c > 0:
        pod_item_number = randrange(1,c+1)
        print("Going to kill pod number [%s] of [%s]" % ( str(pod_item_number), str(c) ) )
        pod_item = pod_list.items[pod_item_number-1]
        v1.delete_namespaced_pod(pod_item.metadata.name, namespace)
      else:
        print("Skipping, as no pods were found in namespace [%s]" % ( namespace ) )

      print("Sleeping for [%s] seconds ..." % ( interval ) )
      sleep(int(interval))


if __name__ == '__main__':
    main()
