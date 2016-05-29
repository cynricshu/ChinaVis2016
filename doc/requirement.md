1.
Les Misérables Co-occurrence
1)	遍历Subject
2)	group by Subject
3)	返回数据所有与该Subject相关的发件人或收件人名称如下格式：
[{name: "Myriel", group: 1}, {name: "Napoleon", group: 1},…]
4)	找出所有发件人和收件人之间的邮件来往量并返回以个格式：
[{source: 1, target: 0, value: 1}, {source: 2, target: 0, value: 8},…]
	
2. 
Radial Reingold–Tilford Tree
找到所有cc的父子关系，然后merge同一个人或组织的父子关系返回以下格式json:
{
 "name": "liyichun",
 "children": [
  {
   "name": "analytics",
   "children": [
    {
     "name": "cluster",
     "children": [
      {"name": "AgglomerativeCluster", "size": 3938},
      {"name": "CommunityStructure", "size": 3812},
      {"name": "HierarchicalCluster", "size": 6714},
      {"name": "MergeEdge", "size": 743}
     ]
    },
    {
     "name": "graph",
     "children": [
      {"name": "BetweennessCentrality", "size": 3534},
      {"name": "LinkDistance", "size": 5731},
      {"name": "MaxFlowMinCut", "size": 7840},
      {"name": "ShortestPaths", "size": 5914},
      {"name": "SpanningTree", "size": 3416}
     ]
    },
    {
     "name": "optimization",
     "children": [
      {"name": "AspectRatioBanker", "size": 7074}
     ]
    }
   ]
  }
 ]
}


3. 
Force-based label placement
统计所以	from to 的importance（importance相加）
返回数据格式如下：
[{source: 1, target: 0, weight: 1}, {source: 2, target: 0, weight: 8},…]

