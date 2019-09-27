import sys
from cmd import Cmd

class txnBlock(object):
    """
    Defines the transaction block object
    Stores transaction block in a queue, for eventual commit
    """

    def __init__(self):
        self.txns = []
    
    def queue(self,command,*args):
        """
        Appends the key/val store's functions and corresponding args
        """
        self.txns.append((command,args))

    def execute(self):
        """
        Call each function along with the argument(s)
        """
        for txn in self.txns:
            txn[0](*txn[1])

    def txn_count(self):
        """
        Return transaction count in the queue
        """
        return len(self.txns)


class simpleStore(object):
    """
    Simple in-memory key/value store that supports transaction blocks
    """
    def __init__(self):
        self.db = {}
        self.blocks = []

    def get(self,key):
        """ 
        retrieve value of a key
        :returns: True if successful
        """
        if self.has_block():
            block = self.blocks[-1]
            block.queue(self.get,key)
        else:
            try:
                return self.db[key]
            except KeyError:
                return False

    def set(self,key,value):
        """ 
        set the value of a key
        :returns: True if successful
        """
        if self.has_block():
            block = self.blocks[-1]
            block.queue(self.set,key,value)
        else:
            if isinstance(key,str):
                self.db[key] = value
                return True
            else:
                return False

    def incr(self,key):
        """ 
        increments a value
        :returns: True if successful
        """

        if self.has_block():
            block = self.blocks[-1]
            block.queue(self.incr,key)
        else:
            if isinstance(key,str):
                value = self.get(key)
                if not value:
                    value = 1
                else:
                    value += 1
                self.set(key,value)
                return True
            else:
                return False

    def delete(self,key):
        """ 
        Deletes a key
        :returns: True if key exists
        """
        if self.has_block():
            block = self.blocks[-1]
            block.queue(self.delete,key)
        else:
            if not key in self.db:
                return False
            del self.db[key]
            return True

    def delvalue(self,value):
        """ 
        Deletes all keys with specific value
        :returns: Nothing, modifies db if value exists
        """
        if self.has_block():
            block = self.blocks[-1]
            block.queue(self.delvalue,value)
        else:
            self.db = {key:val for key,val in self.db.items() if val != value}

    def has_block(self):
        """
        Check if there is an existing transaction block
        """
        return len(self.blocks) != 0

    def flush(self):
        """
        Discards existing transactions in the block
        :returns: # of txns if block exists, 0 otherwise
        """
        if len(self.blocks) != 0:
            txn_len = self.blocks[-1].txn_count()
            self.blocks[-1].txns = []
            return txn_len
        else:
            return 0

    def start_block(self):
        """
        Starts a new transaction block
        """
        self.blocks.append(txnBlock())

    def exec_block(self):
        """
        Execute transaction block
        :returns: # of txns if block exists, 0 otherwise
        """
        if len(self.blocks) != 0:
            txn_len = self.blocks[-1].txn_count()
            self.blocks.pop().execute()
            return txn_len
        else:
            return 0     


class DB(Cmd,object):
    """
    Wrapper with CLI around simpleStore
    CLI command support through python's built-in cmd package
    """

    def __init__(self, *args, **kwargs):
        super(DB, self).__init__(*args, **kwargs)
        self.db = simpleStore()

    def do_GET(self, args):
        """
        Get Value from store based on key
        """
        lst = list(args.split())
        if len(lst) == 0:
            print('missing key')
        else:
            key = lst[0]
            if (self.db.get(key)):
                print(self.db.get(key))
            else:
                if not self.db.has_block():
                    print('<nil>')

    def do_SET(self, args):
        """
        Set Key/Value in Store
        """
        lst = list(args.split())
        if len(lst) != 2:
            print('missing key/value')
        else:
            key = lst[0]
            value = int(lst[1])
            self.db.set(key,value)

    def do_INCR(self, args):
        """
        Increment Value in Store
        """
        lst = list(args.split())
        if len(lst) != 1:
            print('missing key')
        else:
            key = lst[0]
            self.db.incr(key)

    def do_DEL(self,args):
        """
        Delete Value in Store
        """
        lst = list(args.split())
        if len(lst) != 1:
            print('missing key')
        else:
            key = lst[0]
            self.db.delete(key)

    def do_DELVALUE(self,args):
        """
        Delete Keys with given Value in Store
        """
        lst = list(args.split())
        if len(lst) != 1:
            print('missing value')
        else:
            value = int(lst[0])
            self.db.delvalue(value)

    def do_MULTI(self,args):
        """
        starts a transaction block
        """
        self.db.start_block()

    def do_EXEC(self,args):
        """
        Commits a transaction block
        """
        txn_count = self.db.exec_block()
        if (txn_count != 0):
            print(txn_count)
        else:
            print("NOT IN TRANSACTION")

    def do_DISCARD(self,args):
        """
        discards  transaction block
        """
        txn_count = self.db.flush()
        if(txn_count != 0):
            print(txn_count)
        else:
            print("NOT IN TRANSACTION")

    def do_quit(self, args):
        """
        Quits the program
        """
        print("Quitting")
        raise SystemExit

def main():
    prompt = DB()
    prompt.prompt = '> '
    prompt.cmdloop('...Simple Key/Value Store...\n...Type help for options...')

if __name__ == "__main__":
    main()
