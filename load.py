#!/usr/bin/env python3

from neo4jrestclient.client import GraphDatabase
from neo4jrestclient.query import Q
import json

def cluster(db,uuid,name):
                lookup = Q("UUID", exact="%s" %uuid)
                cl = db.nodes.filter(lookup)
                if len(cl) < 1:
                                lblcl = db.labels.create("Cluster")
                                cl1 = db.nodes.create()
                                cl1['Name'] = name
                                cl1['UUID'] = uuid
                                lblcl.add(cl1)
                                return cl1
                return cl[0]


def project(db,uuid,name):
                lookup = Q("UUID", exact="%s" %uuid)
                prjs = db.nodes.filter(lookup)
                if len(prjs) < 1:
                                lblprj = db.labels.create("Project")
                                prj = db.nodes.create()
                                prj['Name'] = name
                                prj['UUID'] = uuid
                                lblprj.add(prj)
                                return prj
                return prjs[0]

def linkPrjVm(db,prj,vm,link):
                lookup = Q("Name", exact="%s" %link)
                rel = db.relationships.filter(lookup)
                found = False
                for e in rel:
                    if e.start.id == vm.id:
                        found = True
                if not found:
                    rel = vm.relationships.create(link, prj)
                    rel['Name']=link

def linkClusVm(db,cluster,vm,link):
                lookup = Q("Name", exact="%s" %link)
                rel = db.relationships.filter(lookup)
                found = False
                for e in rel:
                    if e.start.id == vm.id:
                        found = True
                if not found:
                    rel = vm.relationships.create(link,cluster)
                    rel['Name'] = link




def vm(db,uuid,name):
                lookup= Q("UUID", exact="%s" %uuid)
                vml = db.nodes.filter(lookup)
                if len(vml) < 1:
                                lblvm = db.labels.create("VM")
                                v = db.nodes.create()
                                v['Name'] = name
                                v['UUID'] = uuid
                                lblvm.add(v)
                                return v
                return vml[0]




def main():
                db = GraphDatabase("http://localhost:7474", username="neo4j", password="nutanix/4u")

                config = json.loads(open('vm.json').read())


                for e in config['entities']:
                                spec = e['spec']
                                clus = spec['cluster_reference']
                                cl = cluster(db,clus['uuid'],clus['name'])
                                meta = e['metadata']
                                uuid = meta['uuid']
                                name = spec['name']
                                vml = vm(db,uuid,name)
                                vml['teste'] = "teste"
                                linkClusVm(db,cl,vml,"is Hosted in")
                                if "project_reference" in meta:
                                    proj = meta['project_reference']
                                    projname = proj['name']
                                    projuuid = proj['uuid']
                                    prj = project(db,projuuid,projname)
                                    uuid = meta['uuid']
                                    name = spec['name']
                                    linkPrjVm(db,prj,vml,"in a Project")







if __name__ == "__main__":
                main()
