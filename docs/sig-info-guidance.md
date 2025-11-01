

# Ascend项目社区SIG组权限管理方案

## 介绍
Ascend管理多个项目，每个项目有自己的技术委员会和SIG组，SIG成员和仓库管理需要规范管理。

Ascend组织基于**Community代码仓库**，实现Ascend组织的**项目、SIG、仓库、成员及其权限的统一管理**。

community仓库中infrastructure的**community**SIG组的sig-info.yaml管理community仓库的PR合入权限。




## 关键角色配置
角色|	字段|	权限范围|
|------|----------|----------|
|Committer|	committers |	代码合并权限（可覆盖到文件级）|
|Reviewer|	reviewers	| 代码评审权限（可覆盖到文件级），可按需配置 |
|分支守护者|	branch_keeper |	特定分支版本管理（打keeper_approved标签）|


## sig-info.yaml文件指导说明

###  sig-info.yaml 文件格式

sig-info.yaml 文件为yaml格式承载，主要包含如下一层基本元素：
| 字段 | 类型 |层级| 说明 |
|--|--|--|--|
| name | 字符串 |一层| SIG组名称 |
| description |  字符串 |一层| SIG组描述信息 |
| mailing_list | 字符串 |一层| SIG组讨论邮件列表地址 |
| meeting_url |  字符串 |一层| SIG例会纪要URL |
| committers| 列表 | 一层|SIG组对应的committer名单 |
| reviewers| 列表 | 一层|SIG组对应的reviewer名单，可按需设置 |
| repositories| 列表 |一层| SIG组所管辖的代码仓库信息 |

其中 repositories 字段会说明SIG组所管理的组的信息，repositories列表中的每一条记录可包含如下元素：
| 字段 | 类型 |层级| 说明 |
|--|--|--|--|
| repo| 列表|二层 | 仓库组，可以是一个仓库，也可以是一组仓库 ，可选|
| committers| 列表 |二层 | 仓库组对应的committer名单 ，可选|
| reviewers| 列表 |二层 | 仓库组对应的reviewer名单 ，可选|
| branch_configs | 列表 |二层| 分支列表, 可选 |
| entry_configs | 列表 |二层 | 仓库下的目录或文件配置 ，可选|

上述branch_configs 列表中的每一条记录可包含如下元素：
| 字段 | 类型 | 层级|说明 |
|--|--|--|--|
| branch | 列表 |三层| 分支列表, 可选 |
| committers| 列表 |三层| 仓库对应分支下的committer名单, 可选 |
| reviewers| 列表 |三层| 仓库对应分支下的reviewer名单, 可选 |
| branch_keeper| 列表 |三层| 仓库对应分支下的branch_keeper名单, 可选 |
| entry_configs | 列表 |三层 | 仓库对应分支下的目录或文件配置 ，可选|

上述entry_configs 列表中的每一条记录可包含如下元素：
| 字段 | 类型 | 层级|说明 |
|--|--|--|--|
| path | 列表 |-| 目录或者文件列表, 可选 |
| committers| 列表 |-| 目录或者文件列表下的committer名单, 可选 |
| reviewers| 列表 |-| 目录或者文件列表下的reviewer名单, 可选 |

上述mentors、committers、reviewers、branch_keeper、contributors的每一条个人信息记录包含如下元素：
| 字段 | 类型 | 层级|说明 |
|--|--|--|--|
| gitcode_id | 字符串 |-| gitcode ID, 必填 |
| name | 字符串 |-| 姓名(或者网名), 可选 |
| email| 字符串 |-|  个人邮箱地址, 可选 |

### 下面介绍在以下几种场景sig-info.yaml应该怎么配置
#### 1.只有sig组的committers和reviewers，sig组下各仓库不单独设置committers和reviewers,branch_keeper配置是可选的
```yaml
name: MindIE                          #SIG组名称
description: This is a sample sig.    #SIG组描述信息
mailing_list: mindie@open-ascend.org  #SIG组讨论邮件列表地址
meeting_url: NA                       #SIG例会纪要URL
mentors:                              #SIG组当前导师名单，（SIG组导师负责明确SIG组职责、愿景，促进SIG组内部沟通协作等，和PR合入权限不挂钩）
- gitcode_id: aaa
- gitcode_id: bbb
committers:                           #SIG组所有committer名单 （ccc和ddd拥有MindIE sig组下所有仓库的committer权限）
- gitcode_id: ccc
- gitcode_id: ddd
reviewers:                            #SIG组所有reviewer名单 （eee和fff拥有MindIE sig组下所有仓库的reviewer权限）
- gitcode_id: eee
- gitcode_id: fff
repositories:                         #repositories 字段会说明SIG组所管理的仓库组的信息
- repo:                               #仓库组，可以是一个仓库，也可以是一组仓库 ，可选字段
  - Ascend/MindIE-AAA
  branch_configs:
  - branch:
    - master
    branch_keeper:                    #branch_keeper指仓库某个分支的版本经理角色，此角色有权限对PR评论/merge，打上keeper_approved标签
    - gitcode_id: eee
- repo:                               #仓库组，可以是一个仓库，也可以是一组仓库 ，可选字段
  - Ascend/MindIE-BBB
  branch_configs:
  - branch:
    - master
    branch_keeper:                    #branch_keeper指仓库某个分支的版本经理角色，此角色有权限对PR评论/merge，打上keeper_approved标签
    - gitcode_id: fff
```

#### 2.针对sig组各仓库单独设置committers和reviewers
```yaml
name: MindIE                          #SIG组名称
description: This is a sample sig.    #SIG组描述信息
mailing_list: mindie@open-ascend.org  #SIG组讨论邮件列表地址
meeting_url: NA                       #SIG例会纪要URL
mentors:                              #SIG组当前导师名单，和PR合入无关
- gitcode_id: aaa
- gitcode_id: bbb
committers:                           #SIG组所有committer名单 （ccc和ddd拥有MindIE sig组下除了MindIE-AAA、MinIE-BBB仓库以外的其它仓库的committer权限）
- gitcode_id: ccc
- gitcode_id: ddd
reviewers:                            #SIG组所有reviewer名单 （eee和fff拥有MindIE sig组下除了MindIE-AAA、MinIE-BBB仓库以外的其它仓库的reviewer权限）
- gitcode_id: eee
- gitcode_id: fff
repositories:                         #repositories 字段会说明SIG组所管理的仓库组的信息
- repo:                               #仓库组，可以是一个仓库，也可以是一组仓库 ，可选字段
  - Ascend/MindIE-AAA
  - Ascend/MindIE-BBB
  committers:                         #仓库组对应的committer名单 ，可选字段 （ggg和hhh拥有MindIE-AAA、MinIE-BBB仓库的committer权限）
  - gitcode_id: ggg
  - gitcode_id: hhh
  reviewers:                          #仓库组对应的reviewer名单 ，可选字段 （iii和jjj拥有MindIE-AAA、MinIE-BBB仓库的reviewer权限）
  - gitcode_id: iii
  - gitcode_id: jjj
- repo:                               #仓库组，可以是一个仓库，也可以是一组仓库 ，可选字段
  - Ascend/MindIE-CCC
  - Ascend/MindIE-DDD
  committers:                         #仓库组对应的committer名单 ，可选字段 （ggg和hhh拥有MindIE-CCC、MinIE-DDD仓库的committer权限）
  - gitcode_id: kkk
  - gitcode_id: lll
  reviewers:                          #仓库组对应的reviewer名单 ，可选字段 （iii和jjj拥有MindIE-CCC、MinIE-DDD仓库的reviewer权限）
  - gitcode_id: mmm
  - gitcode_id: nnn
```

#### 3.针对sig组各仓库单独设置committers和reviewers,并且针对仓库所有分支设置某个目录或者文件的committers和reviewers
```yaml
name: MindIE                          #SIG组名称
description: This is a sample sig.    #SIG组描述信息
mailing_list: mindie@open-ascend.org  #SIG组讨论邮件列表地址
meeting_url: NA                       #SIG例会纪要URL
mentors:                              #SIG组当前导师名单
- gitcode_id: aaa
- gitcode_id: bbb
committers:                           #SIG组所有committer名单
- gitcode_id: ccc
- gitcode_id: ddd
reviewers:                            #SIG组所有reviewer名单
- gitcode_id: eee
- gitcode_id: fff
repositories:                         #repositories 字段会说明SIG组所管理的仓库组的信息
- repo:                               #仓库组，可以是一个仓库，也可以是一组仓库 ，可选字段
  - Ascend/MindIE-AAA
  - Ascend/MindIE-BBB
  committers:                         #仓库组对应的committer名单 ，可选字段 （ggg和hhh拥有MindIE-AAA、MinIE-BBB仓库下除了cmake/figures目录和siginfo.yaml文件的committer权限）
  - gitcode_id: ggg
  - gitcode_id: hhh
  reviewers:                          #仓库组对应的reviewer名单 ，可选字段 （ggg和hhh拥有MindIE-AAA、MinIE-BBB仓库下除了cmake/figures目录和siginfo.yaml文件的reviewer权限）
  - gitcode_id: iii
  - gitcode_id: jjj
  entry_configs:                      #(repo)entry_configs字段会说明仓库组所管理的entry组的信息
  - path:                             #entry组，可以是一个目录或者完整的文件路径，也可以是一组目录或者完整的文件路径，可选字段
    - cmake/figures
    - siginfo.yaml
    committers:                       #entry组对应的committer名单 ，可选字段 （yyy和zzz拥有MindIE-AAA、MinIE-BBB仓库下cmake/figures目录和siginfo.yaml文件的committer权限）
    - gitcode_id: yyy
    - gitcode_id: zzz
    reviewers:                        #entry组对应的reviewer名单 ，可选字段 （qwe和rty拥有MindIE-AAA、MinIE-BBB仓库下cmake/figures目录和siginfo.yaml文件的reviewer权限）
    - gitcode_id: qwe
    - gitcode_id: rty
  - path:                             #entry组，可以是一个目录或者完整的文件路径，也可以是一组目录或者完整的文件路径，可选字段
    - debug/validate
    - setup.py
    committers:                        #entry组对应的committer名单 ，可选字段 （yyy和zzz拥有MindIE-AAA、MinIE-BBB仓库下cmake/figures目录和siginfo.yaml文件的committer权限）
    - gitcode_id: uio
    - gitcode_id: asd
    reviewers:                        #entry组对应的reviewer名单 ，可选字段 （qwe和rty拥有MindIE-AAA、MinIE-BBB仓库下cmake/figures目录和siginfo.yaml文件的reviewer权限）
    - gitcode_id: fgh
    - gitcode_id: jkl
  
```

#### 4.针对sig组各仓库单独设置committers和reviewers,并且针对仓库某些分支设置committers和reviewers
```yaml
name: MindIE                          #SIG组名称
description: This is a sample sig.    #SIG组描述信息
mailing_list: mindie@open-ascend.org  #SIG组讨论邮件列表地址
meeting_url: NA                       #SIG例会纪要URL
mentors:                              #SIG组当前导师名单
- gitcode_id: aaa
- gitcode_id: bbb
committers:                           #SIG组所有committer名单
- gitcode_id: ccc
- gitcode_id: ddd
reviewers:                            #SIG组所有reviewer名单
- gitcode_id: eee
- gitcode_id: fff
repositories:                         #repositories 字段会说明SIG组所管理的仓库组的信息
- repo:                               #仓库组，可以是一个仓库，也可以是一组仓库 ，可选字段
  - Ascend/MindIE-AAA
  - Ascend/MindIE-BBB
  committers:                         #仓库组对应的committer名单 ，可选字段 （ggg和hhh拥有MindIE-AAA、MinIE-BBB仓库除了master、br_release分支的committer权限）
  - gitcode_id: ggg
  - gitcode_id: hhh
  reviewers:                          #仓库组对应的reviewer名单 ，可选字段 （iii和jjj拥有MindIE-AAA、MinIE-BBB仓库除了master、br_release分支的reviewer权限）
  - gitcode_id: iii
  - gitcode_id: jjj
  branch_configs:                     #branch_configs 字段会说明仓库组所管理的分支组的信息
  - branch:                           #分支组，可以是一个分支，也可以是一组分支，可选字段
    - master
    - br_release
    committers:                       #分支组对应的committer名单 ，可选字段 （kkk和LLL拥有MindIE-AAA、MinIE-BBB仓库master、br_release分支的committer权限）
    - gitcode_id: kkk
    - gitcode_id: LLL
    reviewers:                        #分支组对应的reviewer名单 ，可选字段 （mmm和nnn拥有MindIE-AAA、MinIE-BBB仓库master、br_release分支的reviewer权限）
    - gitcode_id: mmm
    - gitcode_id: nnn
    branch_keeper:                    #分支组对应的branch_keeper名单 ，可选字段
    - gitcode_id: ooo
  - branch:                           #分支组，可以是一个分支，也可以是一组分支，可选字段
    - develop
    - feature
    committers:                       #分支组对应的committer名单 ，可选字段 （kkk和LLL拥有MindIE-AAA、MinIE-BBB仓库master、br_release分支的committer权限）
    - gitcode_id: zzz
    - gitcode_id: xxx
    reviewers:                        #分支组对应的reviewer名单 ，可选字段 （mmm和nnn拥有MindIE-AAA、MinIE-BBB仓库master、br_release分支的reviewer权限）
    - gitcode_id: ccc
    - gitcode_id: vvv
    branch_keeper:                    #分支组对应的branch_keeper名单 ，可选字段
    - gitcode_id: qqq
```

#### 5.针对sig组各仓库单独设置committers和reviewers，仓库某些分支设置committers和reviewers，并且在这些分支下设置某个目录或者文件的committers和reviewers
```yaml
name: MindIE                          #SIG组名称
description: This is a sample sig.    #SIG组描述信息
mailing_list: mindie@open-ascend.org  #SIG组讨论邮件列表地址
meeting_url: NA                       #SIG例会纪要URL
mentors:                              #SIG组当前导师名单
- gitcode_id: aaa
- gitcode_id: bbb
committers:                           #SIG组所有committer名单
- gitcode_id: ccc
- gitcode_id: ddd
reviewers:                            #SIG组所有reviewer名单
- gitcode_id: eee
- gitcode_id: fff
repositories:                         #repositories 字段会说明SIG组所管理的仓库组的信息
- repo:                               #仓库组，可以是一个仓库，也可以是一组仓库 ，可选字段
  - Ascend/MindIE-AAA
  - Ascend/MindIE-BBB
  committers:                         #仓库组对应的committer名单 ，可选字段
  - gitcode_id: ggg
  - gitcode_id: hhh
  reviewers:                          #仓库组对应的reviewer名单 ，可选字段
  - gitcode_id: iii
  - gitcode_id: jjj
  branch_configs:                     #branch_configs 字段会说明仓库组所管理的分支组的信息
  - branch:                           #分支组，可以是一个分支，也可以是一组分支，可选字段
    - master
    - br_release
    committers:                       #分支组对应的committer名单 ，可选字段
    - gitcode_id: kkk
    - gitcode_id: LLL
    reviewers:                        #分支组对应的reviewer名单 ，可选字段
    - gitcode_id: mmm
    - gitcode_id: nnn
    branch_keeper:                    #分支组对应的branch_keeper名单 ，可选字段
    - gitcode_id: ooo
    entry_configs:                    #(branch)entry_configs字段会说明分支组所管理的entry组的信息
    - path:                           #entry组，可以是一个目录或者完整的文件路径，也可以是一组目录或者完整的文件路径，可选字段
      - cmake/figures
      - siginfo.yaml
      committers:                     #entry组对应的committer名单 ，可选字段 （qqq和rrr拥有MindIE-AAA、MinIE-BBB仓库master和br_release分支下cmake/figures目录和siginfo.yaml文件的committer权限）
      - gitcode_id: qqq
      - gitcode_id: rrr
      reviewers:                      #entry组对应的reviewer名单 ，可选字段 （sss和ttt拥有MindIE-AAA、MinIE-BBB仓库master和br_release分支下cmake/figures目录和siginfo.yaml文件的reviewr权限）
      - gitcode_id: sss
      - gitcode_id: ttt
    - path:                           #entry组，可以是一个目录或者完整的文件路径，也可以是一组目录或者完整的文件路径，可选字段
      - debug/validate
      - setup.py
      committers:                     #entry组对应的committer名单 ，可选字段 （qqq和rrr拥有MindIE-AAA、MinIE-BBB仓库master和br_release分支下cmake/figures目录和siginfo.yaml文件的committer权限）
      - gitcode_id: uuu
      - gitcode_id: vvv
      reviewers:                      #entry组对应的reviewer名单 ，可选字段 （sss和ttt拥有MindIE-AAA、MinIE-BBB仓库master和br_release分支下cmake/figures目录和siginfo.yaml文件的reviewr权限）
      - gitcode_id: www
      - gitcode_id: xxx
  - branch:                           #分支组，可以是一个分支，也可以是一组分支，可选字段
    - develop
    - feature
    committers:                       #分支组对应的committer名单 ，可选字段
    - gitcode_id: kkk
    - gitcode_id: LLL
    reviewers:                        #分支组对应的reviewer名单 ，可选字段
    - gitcode_id: mmm
    - gitcode_id: nnn
    branch_keeper:                    #分支组对应的branch_keeper名单 ，可选字段
    - gitcode_id: ooo
    entry_configs:                    #(branch)entry_configs字段会说明分支组所管理的entry组的信息
    - path:                           #entry组，可以是一个目录或者完整的文件路径，也可以是一组目录或者完整的文件路径，可选字段
      - cmake/figures
      - siginfo.yaml
      committers:                     #entry组对应的committer名单 ，可选字段 （qqq和rrr拥有MindIE-AAA、MinIE-BBB仓库master和br_release分支下cmake/figures目录和siginfo.yaml文件的committer权限）
      - gitcode_id: qqq
      - gitcode_id: rrr
      reviewers:                      #entry组对应的reviewer名单 ，可选字段 （sss和ttt拥有MindIE-AAA、MinIE-BBB仓库master和br_release分支下cmake/figures目录和siginfo.yaml文件的reviewr权限）
      - gitcode_id: sss
      - gitcode_id: ttt
    - path:                           #entry组，可以是一个目录或者完整的文件路径，也可以是一组目录或者完整的文件路径，可选字段
      - debug/validate
      - setup.py
      committers:                     #entry组对应的committer名单 ，可选字段 （qqq和rrr拥有MindIE-AAA、MinIE-BBB仓库master和br_release分支下cmake/figures目录和siginfo.yaml文件的committer权限）
      - gitcode_id: uuu
      - gitcode_id: vvv
      reviewers:                      #entry组对应的reviewer名单 ，可选字段 （sss和ttt拥有MindIE-AAA、MinIE-BBB仓库master和br_release分支下cmake/figures目录和siginfo.yaml文件的reviewr权限）
      - gitcode_id: www
      - gitcode_id: xxx
```
### sig-info.yaml 完整样例：
```yaml
name: MindIE                          #SIG组名称
description: This is a sample sig.    #SIG组描述信息
mailing_list: mindie@open-ascend.org  #SIG组讨论邮件列表地址
meeting_url: NA                       #SIG例会纪要URL
mentors:                              #SIG组当前导师名单
- gitcode_id: aaa
- gitcode_id: bbb
committers:                            #SIG组所有committer名单
- gitcode_id: ccc
- gitcode_id: ddd
reviewers:                            #SIG组所有reviewer名单
- gitcode_id: eee
- gitcode_id: fff
repositories:                         #repositories 字段会说明SIG组所管理的仓库组的信息
- repo:                               #仓库组，可以是一个仓库，也可以是一组仓库 ，可选字段
  - Ascend/MindIE-AAA
  - Ascend/MindIE-BBB
  committers:                          #仓库组对应的committer名单 ，可选字段
  - gitcode_id: ggg
  - gitcode_id: hhh
  reviewers:                          #仓库组对应的reviewer名单 ，可选字段
  - gitcode_id: iii
  - gitcode_id: jjj
  entry_configs:                      #(repo)entry_configs字段会说明仓库组所管理的entry组的信息
  - path:                             #entry组，可以是一个目录或者完整的文件路径，也可以是一组目录或者完整的文件路径，可选字段
    - cmake/figures
    - cmake/utils
    committers:                        #entry组对应的committer名单 ，可选字段
    - gitcode_id: yyy
    - gitcode_id: zzz
    reviewers:                        #entry组对应的reviewer名单 ，可选字段
    - gitcode_id: qwe
    - gitcode_id: rty
  - path: 									
    - siginfo.yaml
    - cmake/utils/setup.py
    committers: 								
    - gitcode_id: uio
    - gitcode_id: asd
    reviewers:								
    - gitcode_id: fgh
    - gitcode_id: jkl
  branch_configs:                     #branch_configs 字段会说明仓库组所管理的分支组的信息
  - branch:                           #分支组，可以是一个分支，也可以是一组分支，可选字段
    - master
    - br_release
    committers:                        #分支组对应的committer名单 ，可选字段
    - gitcode_id: kkk
    - gitcode_id: LLL
    reviewers:                        #分支组对应的reviewer名单 ，可选字段
    - gitcode_id: mmm
    - gitcode_id: nnn
    branch_keeper:                    #分支组对应的branch_keeper名单 ，可选字段
    - gitcode_id: ooo
    - gitcode_id: ppp
    entry_configs:                    #(branch)entry_configs字段会说明分支组所管理的entry组的信息
    - path:                           #entry组，可以是一个目录或者完整的文件路径，也可以是一组目录或者完整的文件路径，可选字段
      - cmake/figures
      - cmake/utils
      committers:                      #entry组对应的committer名单 ，可选字段
      - gitcode_id: qqq
      - gitcode_id: rrr
      reviewers:                      #entry组对应的reviewer名单 ，可选字段
      - gitcode_id: sss
      - gitcode_id: ttt
    - path:
      - siginfo.yaml
      - cmake/utils/setup.py
      committers: 							
      - gitcode_id: uuu
      - gitcode_id: vvv
      reviewers:							
      - gitcode_id: www
      - gitcode_id: xxx
  - branch:                           #分支组，可以是一个分支，也可以是一组分支，可选字段
    - develop
    - feature
    committers:                       #分支组对应的committer名单 ，可选字段
    - gitcode_id: kkk
    - gitcode_id: LLL
    reviewers:                        #分支组对应的reviewer名单 ，可选字段
    - gitcode_id: mmm
    - gitcode_id: nnn
    branch_keeper:                    #分支组对应的branch_keeper名单 ，可选字段
    - gitcode_id: ooo
    entry_configs:                    #(branch)entry_configs字段会说明分支组所管理的entry组的信息
    - path:                           #entry组，可以是一个目录或者完整的文件路径，也可以是一组目录或者完整的文件路径，可选字段
      - cmake/figures
      - siginfo.yaml
      committers:                     #entry组对应的committer名单 ，可选字段 （qqq和rrr拥有MindIE-AAA、MinIE-BBB仓库master和br_release分支下cmake/figures目录和siginfo.yaml文件的committer权限）
      - gitcode_id: qqq
      - gitcode_id: rrr
      reviewers:                      #entry组对应的reviewer名单 ，可选字段 （sss和ttt拥有MindIE-AAA、MinIE-BBB仓库master和br_release分支下cmake/figures目录和siginfo.yaml文件的reviewr权限）
      - gitcode_id: sss
      - gitcode_id: ttt
    - path:                           #entry组，可以是一个目录或者完整的文件路径，也可以是一组目录或者完整的文件路径，可选字段
      - debug/validate
      - setup.py
      committers:                     #entry组对应的committer名单 ，可选字段 （qqq和rrr拥有MindIE-AAA、MinIE-BBB仓库master和br_release分支下cmake/figures目录和siginfo.yaml文件的committer权限）
      - gitcode_id: uuu
      - gitcode_id: vvv
      reviewers:                      #entry组对应的reviewer名单 ，可选字段 （sss和ttt拥有MindIE-AAA、MinIE-BBB仓库master和br_release分支下cmake/figures目录和siginfo.yaml文件的reviewr权限）
      - gitcode_id: www
      - gitcode_id: xxx  
```

