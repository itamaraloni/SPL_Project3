class Vaccine:
    def __init__(self, id, date, supplier, quantity):
        self.id = id
        self.date = date
        self.supplier = supplier
        self.quantity = quantity

    def _str_(self):
        return str(tuple([self.id, self.date, self.supplier, self.quantity]))


class Supplier:
    def __init__(self, id, name, logistic):
        self.id = id
        self.name = name
        self.logistic = logistic

    def _str_(self):
        return str(tuple([self.id, self.name, self.logistic]))



class Clinic:
    def __init__(self, id, location, demand, logistic):
        self.id = id
        self.location = location
        self.demand = demand
        self.logistic = logistic

    def _str_(self):
        return str(tuple([self.id, self.location, self.demand, self.logistic]))


class Logistic:
    def __init__(self, id, name, count_sent, count_received):
        self.id = id
        self.name = name
        self.count_sent = count_sent
        self.count_received = count_received

    def _str_(self):
        return str(tuple([self.id, self.name, self.count_sent, self.count_received]))