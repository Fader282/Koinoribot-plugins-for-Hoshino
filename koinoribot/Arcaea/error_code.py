
def getErrorDesc(message: str):
    if message == 'invalid username or usercode':
        return '玩家名字或者好友码不对喔'
    elif message == 'invalid usercode':
        return '好友码不对喔'
    elif message == 'user not found':
        return '没有找到这个玩家...'
    elif message == 'too many users':
        return '玩家太多了...'
    elif message == 'invalid songname or songid':
        return '歌曲名字或者ID不对喔'
    elif message == 'invalid songid':
        return '歌曲ID不对喔'
    elif message == 'song not recorded':
        return '这首曲子没有记录...'
    elif message == 'too many records':
        return '记录太多了...'
    elif message == 'invalid difficulty':
        return '难度不对喔'
    elif message == 'invalid recent/overflow number':
        return 'recent值/overflow值不对喔'
    elif message == 'allocate an arc account failed':
        return '分配arcaea账户失败(这是什么...?)'
    elif message == 'clear friend failed':
        return '清除好友失败了...'
    elif message == 'add friend failed':
        return '添加好友失败了...'
    elif message == 'this song has no this level':
        return '这首歌没有这个难度喔'
    elif message == 'not played yet':
        return '可能还没有玩过这首歌...'
    elif message == 'user got shadowbanned':
        return 'user got shadowbanned'
    elif message == 'querying best30 failed':
        return 'querying best30 failed'
    elif message == 'update service unavailable':
        return 'update service unavailable'
    elif message == 'invalid partner':
        return 'invalid partner'
    elif message == 'file unavailable':
        return 'file unavailable'
    elif message == 'invalid range':
        return 'invalid range'
    elif message == 'range of rating end smaller than its start':
        return 'range of rating end smaller than its start'
    elif message == 'potential is below the threshold of querying best30 (7.0)':
        return 'potential is below the threshold of querying best30 (7.0)'
    elif message == 'need to update arcaea, please contact maintainer':
        return 'need to update arcaea, please contact maintainer'
    elif message == 'invalid version':
        return 'invalid version'
    elif message == 'daily query quota exceeded':
        return 'daily query quota exceeded'
    elif message == 'illegal hash, please contact maintainer':
        return 'illegal hash, please contact maintainer'
    elif message == 'internal error occurred':
        return 'internal error occurred'
    else:
        return 'unknown error status'
