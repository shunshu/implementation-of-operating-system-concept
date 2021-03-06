'''
    pfs.py is a toy file system in python.
'''

from cntlblks import *

class PFS:
    def __init__(self, nBlocks=16, nDirs=32, nFCBs=64):
        '''
            nBlocks is an int for the number of blocks in this file system (for user)
            root is the directory control block of the root and
            has the link to some initial directories.
        '''
        # - on-disk structure, assuming one partition:
        #   - list of directory control blocks (more like a tree)
        #   - list of file control blocks
        self.nBlocks = nBlocks

        self.FCBs = [ ] # file control blocks
        self.freeBlockSet = set(range(nBlocks))
        self.freeDEntrys = [DEntry() for i in range(nDirs)]
        self.freeFCBs = [FCB() for i in range(nFCBs)]

        self.root = self.allocDEntry()

        # - in-memory structure
        #   - in-memory directory structure
        #   - system-wide open file table
        #   - per-process open file table
        self.sysOpenFileTable = []
        self.sysOpenFileCount = []

        self.storage = [None for i in range(nBlocks)]  # physical storage


    def allocFCB(self):
        f = self.freeFCBs.pop()
        FCB.__init__(f)
        return f

    def freeFCB(self, f):
        self.freeFCBs.append(f)

    def allocDEntry(self):
        d = self.freeDEntrys.pop() # recycle
        DEntry.__init__(d)  # start fresh
        return d

    def freeDEntry(self, d):
        self.freeDEntrys.append(d)


    def parsePath(self, path, defaultDir):
        '''
            utility function to convert from file path (absolute or relative)
            to (DEntry, filename).
            If no directory is specified, then the current working directory
            is returned; filename may be None if empty string.
        '''
        t = path.split('/')
        d = self.root
        filename = ''  # by default, name is empty
        if len(t) == 1:
            # no slash = use defaultDir
            d = defaultDir
            return d, t[0]
        elif len(t) > 1:
            # at least we have a slash
            if t[0] == '':
                # start from root
                d = self.root
            else: # relative to current directory
                d = defaultDir.lookup(t[0])
            # remove trailing / if there is one
            if t[-1] == '':
                filename = t.pop()
            for i, n in enumerate(t[1:]):
                member = d.lookup(n)
                if member is None:
                    filename = n
                    break
                if isinstance(member, DEntry):
                    # keep going
                    d = member
                    continue
                if isinstance(member, FCB):
                    # this must be the last
                    if i == len(t[1:]) - 1:
                        filename = n
                        break
                raise ValueError('%s is not a directory' % n)
            # now d points to the directory
            return (d, filename)
        else: # len(t) < 1: not possible
            raise ValueError('split error on %s' % path)


    def createFile(self, name, enclosingDir):
        # @@@ write your code here
        pass
        # allocate a new FCB and update its directory structure:
        # * if default directory is None, set it to root.
        # * if name already exists, raise exception
        # * allocate a new FCB, add it to the enclosing dir by name,
        # * append to the FCB list of the file system.
        # Note: this does not allocate blocks for the file.
        if enclosingDir == None:
            c = self.allocFCB()
            enclosingDir.content.append(c)
        else:
            for i, n in enumerate(enclosingDir.names):
                if n == name:
                    print('This file named "%s" already exists!' % (name))
                    return
            c = self.allocFCB()
            enclosingDir.addFile(c,name)         
            self.FCBs.append(c)


    def createDir(self, name, enclosingDir):
        # @@@ write your code here
        pass
        # create a new directory under name in enclosing directory.
        # * check if name already exists; if so, raise exception.
        # * allocate a DEntry, add it to enclosing directory,
        # * return the new DEntry.
        for i, n in enumerate(enclosingDir.names):
            if n == name:
                print('This directory named "%s/" already exists!' % (name))
                return
        c = self.allocDEntry()
        enclosingDir.addDir(c,name)
        return c

    def deleteFile(self, name, enclosingDir):
        # @@@ write your code here
        pass
        # * lookup the fcb by name in the enclosing directory.
        # * if linkCount is 1 (which means about to be 0 after delete)
        #   and the file is still opened by others, then
        #   raise an exception about unable to delete open files.
        # * call rmFile on enclosingDir to remove the fcb (and name).
        # * if no more linkCount, then 
        #   * recycle free the blocks.
        #   * recycle the fcb
        content = enclosingDir.lookup(name)
        if(content.linkCount == 1 and content.openCount >0):
            print('THis file is opened now!')
        enclosingDir.rmFile(content)
        if content.linkCount == 0:
            c = FCB()
            self.freeFCB(c)
            self.nBlocks += 1

    def deleteDirectory(self, name, enclosingDir):
        # @@@ write your code here
        pass
        # * lookup the dentry by name in the enclosing directory.
        # * if the directory is not empty, raise exception about
        #   unable to delete nonempty directory.
        # * call rmDir on enclosing directory
        # * recycle the dentry 
        dir_content = enclosingDir.lookup(name)
        if len(dir_content.content) >0:
            print('This directory is not empty!')
        enclosingDir.rmDir(dir_content)
        d = DEntry()
        self.freeDEntry(d)

    def rename(self, name, newName, enclosingDir):
        # @@@ write your code here
        pass
        # * check if newName is already in enclosingDir, raise exception
        # * find position of name in names list of enclosingDir
        # * change the name to newName in that list
        # * set last modification time of enclosing directory
        for i, n in enumerate(enclosingDir.names):
            if n == newName:
                print('This file named "%s/" already exists!' % (name))
                return
        for i, n in enumerate(enclosingDir.names):
            if n == name:
                enclosingDir.names[i] = newName
        enclosingDir.updateModTime()

    def move(self, name, fromDir, toDir):
        # @@@ write your code here
        pass
        # * check if name is already in toDir, raise exception
        # * lookup name and see if it is directory or file.
        # * if directory, remove it from fromDir (by calling rmDir),
        #   add it to toDir (by calling addDir)
        # * if file, remove it from fromDir (by calling rmFile)
        #   add it to toDir (by calling addFile)
        for i, n in enumerate(toDir.names):
            if n == name:
                print('This file named "%s/" already exists!' % (name))
                return
        content = fromDir.lookup(name)
        if type(content) == DEntry:
            fromDir.rmDir(name)
            toDir.addDir(content,name)
        elif type(content) == FCB:
            fromDir.rmFile(content)
            toDir.addFile(content, name)


def MakeFSFromTree(fs, tree, root=None):
    '''
        utility function to make directory from tree
    '''
    if tree == ():
        return None
    if isinstance(tree, str):
        fs.createFile(name=tree, enclosingDir=root)
    elif tree[0][-1] == '/':
        if root is None:
            c = fs.root
            root = c
        else:
            # c = root.makeDir(tree[0][:-1])
            name = tree[0][:-1]
            c = fs.createDir(name, enclosingDir=root)
        if len(tree) > 1:
            for t in tree[1:]:
                MakeFSFromTree(fs, t, c)
    return root


if __name__ == '__main__':
    directoryTree = ( '/',  ('home/', ('u1/', 'hello.c', 'myfriend.h'),
                                    ('u2/', 'world.h'), 'homefiles'),
                            ('bin/', 'ls'),
                            ('etc/', ))

    # make an initial directory
    print('input directory tree=%s' % repr(directoryTree))

    fs = PFS(nBlocks = 16)
    root = MakeFSFromTree(fs, directoryTree)
    print('directory=%s' % repr(MakeTreeFromDir(root)))

    d, f = fs.parsePath('/home/u1/', root)
    print('last modification date for /home/u1/ is %s' %  d.modTime)
    time.sleep(5)
    fs.rename('hello.c', 'goodbye.py', d)
    print('after renaming=%s' % repr(MakeTreeFromDir(root)))
    print('last modification date for /home/u1/ is %s' %  d.modTime)
    t, f = fs.parsePath('/home/u2/', root)
    fs.move('myfriend.h', d, t) # from /home/u1 to /home/u2
    print('after moving=%s' % repr(MakeTreeFromDir(root)))
    fs.move('etc', root, d)  # move /etc to /home/u1
    print('after moving=%s' % repr(MakeTreeFromDir(root)))
