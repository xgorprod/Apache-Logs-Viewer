class Api:
    def __init__(self, db):
        self.db = db
        self.cursor = self.db.cursor
        self.connection = self.db.connection
        self.apply_filters = self.db.apply_filters
        self.query = self.db.query

    def viewer(self, filters=None):
        if filters is None: filters = "-"
        apply = self.apply_filters(filters)
        prompt = apply[0] != ''
        fields = apply[1]
        req = f"SELECT {prompt and fields or '*'} FROM Logs"
        self.query(req)
        return self.cursor.fetchall()
    
    def sort_by(self, arg1=None, filters=None, sort_type="ASC"):
        if not arg1: return 
        sort_type = sort_type.upper()
        vari = ["DATE", "DATETIME", "TIMESTAMP"]
        col = "remote_host"
        apply = self.apply_filters(filters)
        prompt = apply[0] != ''
        fields = apply[1]

        que = f"SELECT {prompt and fields or '*'} FROM Logs ORDER BY"
        
        if arg1.upper() in vari:
            col = "request_time"
            req = f'{que} {col} {sort_type}'
        else:
            req = f'{que} {col} {sort_type}'

        self.query(req)
        return self.cursor.fetchall()
    
    def group_by_ip(self, arg1=None, arg2=None, filters=None):
        if not arg1: return 

        col = "remote_host"
        apply = self.apply_filters(filters)
        prompt = apply[0]
        fields = apply[1]

        que = f"SELECT {prompt and fields or '*'} FROM Logs WHERE"

        if arg2 and arg2[1:-1] != filters: 
            req = f'{que} {col} = "{arg1}" AND final_status = {arg2}'
        else:
            req = f'{que} {col} = "{arg1}"'

        self.query(f'{req} ORDER BY {col} ASC')
        return self.cursor.fetchall()
    
    def group_by_date(self, arg1=None, arg2=None, filters=None):
        if not arg1: return 

        col = "request_time"
        apply = self.apply_filters(filters)
        prompt = apply[0]
        fields = apply[1]

        que = f"SELECT {prompt and fields or '*'} FROM Logs WHERE"

        if arg2 and arg2[1:-1] != filters: 
            req = f'{que} {col} BETWEEN "{arg1}" AND "{arg2}" GROUP BY {col}'
        else:
            if len(arg1) == 10:
                req = f'{que} {col} BETWEEN "{arg1} 00:00:00+00:00" AND "{arg1} 23:59:59+00:00" GROUP BY {col}'
            else:
                req = f'{que} {col} = "{arg1}+00:00" GROUP BY {col}'

        self.query(f'{req} ORDER BY {col} ASC')
        return self.cursor.fetchall()
