from kubernetes import client, config
from os import getenv, environ
from sys import exit
from time import sleep

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

      c=0
      for pod in pod_list.items:
        c+=1
        #print("%s\t%s\t%s" % (pod.metadata.name, pod.status.phase, pod.status.pod_ip))

      print("Got [%s] pods from resource of type [%s]" % ( str(c), pod_list.kind ) )

      print("Sleeping for [%s] seconds ..." % ( interval ) )
      sleep(int(interval))


if __name__ == '__main__':
    main()
