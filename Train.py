class Train:
    stations = dict()

    def __init__(self, lst):
        self.stations = {}
        for i in range(1, len(lst), 2):
            try:
                self.stations[int(lst[i])] = lst[i + 1]
            except:
                print("Ошибка ввода. Такой станции не существует!")

    def getStationsCount(self):
        return len(self.stations)

    def getMinutes(self):
        lst = list()
        for i in range(1, int(max(self.stations.keys(), key=int)) + 1):
            try:
                lst.append(self.stations[i])
            except:
                lst.append(None)
        return lst

    def getStations(self):
        return self.stations

    def trainInfo(self):
        print(self.stations)
        print("Поезд останавливается на " + str(self.getStationsCount()) + " станциях")
        print("Поезд идет до станций")

        for i in range(1, int(max(self.stations.keys(), key=int)) + 1):
            try:
                print(str(i) + " " + str(self.stations[i]) + " минут")
            except:
                print(str(i) + " поезд следует без остановки")
                KeyError
