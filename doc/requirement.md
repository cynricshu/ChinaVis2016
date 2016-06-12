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








2016/6/10


第2题

全部
外部邮件可以分成非垃圾邮件和垃圾邮件
内部邮件分为工作邮件和系统邮件
工作邮件分为会议邮件，警告邮件，群发邮件，差旅邮件
格式如下父子包含自己体会

{
  "name": "All Email",
  "children": [
    {
      "name": "outer email",
      "children": [
          {"name": "AgglomerativeCluster",
           "children": [
             {"name": "CommunityStructure", "value": 3812},
             {"name": "HierarchicalCluster", "value": 6714}
           ]
          },
          {"name": "CommunityStructure", "value": 3812},
          {"name": "HierarchicalCluster", "value": 6714},
          {"name": "MergeEdge", "value": 743}
        ]
    },
    {
      "name": "system email",
      "children": [
        {"name": "BetweennessCentrality", "value": 3534},
        {"name": "LinkDistance", "value": 5731},
        {"name": "MaxFlowMinCut", "value": 7840},
        {"name": "ShortestPaths", "value": 5914},
        {"name": "SpanningTree", "value": 3416}
      ]
    }
  ]
}



第3题

图1 

按每年每个topic 计算三维（三维还没想好）
[
  {
    "name": "test1",
    "region": "topic1",
    "income": [
      [2000,2446.65],
      [2001,2479.69],
      [2002,2773.29],
      [2003,2785.39],
      [2004,3007.11],
      [2005,3533],
      [2006,4069.56],
      [2007,4755.46],
      [2008,5228.74],
      [2009,5055.59]
    ],
    "population": [
      [2000,10442812],
      [2001,10623424],
      [2002,10866106],
      [2003, 11186202],
      [2004, 11521432],
      [2005,11827315],
      [2006,12127071],
      [2007,12420476],
      [2008,12707546]
    ],
    "lifeExpectancy": [
      [2000,43.56],
      [2001,43.86],
      [2002,44.22],
      [2003,44.61],
      [2004,45.05],
      [2005,45.52],
      [2006,46.02],
      [2007,46.54],
      [2008,47.06],
      [2009, 47.58]
    ]
  },
  {
    "name": "test2",
    "region": "topic2",
    "income": [
      [2000,1446.65],
      [2001,1479.69],
      [2002,1773.29],
      [2003,1785.39],
      [2004,2007.11],
      [2005,2533],
      [2006,2069.56],
      [2007,2755.46],
      [2008,3228.74],
      [2009,3055.59]
    ],
    "population": [
      [2000,10442812],
      [2001,10623424],
      [2002,10866106],
      [2003, 11186202],
      [2004, 11521432],
      [2005,11827315],
      [2006,12127071],
      [2007,12420476],
      [2008,12707546]
    ],
    "lifeExpectancy": [
      [2000,43.56],
      [2001,43.86],
      [2002,44.22],
      [2003,44.61],
      [2004,45.05],
      [2005,45.52],
      [2006,46.02],
      [2007,46.54],
      [2008,47.06],
      [2009, 47.58]
    ]
  },
  {
    "name": "test3",
    "region": "topic3",
    "income": [
      [2000,2446.65],
      [2001,2479.69],
      [2002,2773.29],
      [2003,2785.39],
      [2004,3007.11],
      [2005,3533],
      [2006,4069.56],
      [2007,4755.46],
      [2008,5228.74],
      [2009,5055.59]
    ],
    "population": [
      [2000,10442812],
      [2001,10623424],
      [2002,10866106],
      [2003, 11186202],
      [2004, 11521432],
      [2005,11827315],
      [2006,12127071],
      [2007,12420476],
      [2008,12707546]
    ],
    "lifeExpectancy": [
      [2000,43.56],
      [2001,43.86],
      [2002,44.22],
      [2003,44.61],
      [2004,45.05],
      [2005,45.52],
      [2006,46.02],
      [2007,46.54],
      [2008,47.06],
      [2009, 47.58]
    ]
  }
]


图2

按每年每月统计每个subject的邮件数量

{"all": {
  "views": [
    [
      {
        "pc": 0.00296
      }，
     ｛
     	“pc”:...
      ｝,
      一下省略其余18个topic（一共20个topic）
    ],
    [
    	...
    ],
    ...一下省略11个月
｝

图3

status可为 importance (SUCCEEDED,RUNNING,FAILED,KILLED)

[
    {"startDate":new Date("Sun Dec 09 01:36:45 EST 2012"),"endDate":new Date("Sun Dec 09 02:36:45 EST 2012"),"taskName":"E Job","status":"RUNNING"},
    {"startDate":new Date("Sun Dec 09 04:56:32 EST 2012"),"endDate":new Date("Sun Dec 09 06:35:47 EST 2012"),"taskName":"A Job","status":"RUNNING"},
    {"startDate":new Date("Sun Dec 09 06:29:53 EST 2012"),"endDate":new Date("Sun Dec 09 06:34:04 EST 2012"),"taskName":"D Job","status":"RUNNING"}]






















