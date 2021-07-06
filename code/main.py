from kubernetes import client, config
from os import getenv

def main():
    config.load_incluster_config()

    namespace = getenv('CM_NAMESPACE')

    print("Getting pods from namespace %s" % namespace)

    v1 = client.CoreV1Api()
    pod_list = v1.list_namespaced_pod(namespace=namespace)
    for pod in pod_list.items:
        print("%s\t%s\t%s" % (pod.metadata.name, pod.status.phase, pod.status.pod_ip))


if __name__ == '__main__':
    main()
