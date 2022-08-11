class Tracker:
    sNumofObjects = 0
    # biraz ileri aşamada dictionary'de sadece center tutmak yerine bounding box koordinatları da tutulabilir
    sCenterCoordinatesofObjects = dict()
    # sDistancestoObjects = dict()

    def __init__(self):
        pass

    @staticmethod
    def register(center):
        Tracker.sNumofObjects += 1
        Tracker.sCenterCoordinatesofObjects[Tracker.sNumofObjects] = center

    @staticmethod
    def deregister(id):
        Tracker.sNumofObjects -= 1
        Tracker.sCenterCoordinatesofObjects.pop(id)

    @staticmethod
    def computeEuclidianDistance(pt1, pt2):
        return ((pt1[0] - pt2[0]) ** 2 + (pt1[0] - pt2[0]) ** 2) ** (1/2)

    @staticmethod
    def update_centers(CurrentCenterCoordinates):
        # 2 ayrı case tanımlamak daha mantıklı gibi, biri frame'e yeni nesnelerin girmiş olma ihtimali
        # diğeri ise frame'den nesnelerin ayrılmış olma ihtimali

        if len(CurrentCenterCoordinates) > len(Tracker.sCenterCoordinatesofObjects):
            # yeni giren nesnenin tespit edilmesi lazım
            for id, center in Tracker.sCenterCoordinatesofObjects:
                ls = [Tracker.computeEuclidianDistance(center, i) for i in CurrentCenterCoordinates]
                min_distance = min(ls)
                min_distance_index = ls.index(min_distance)
                Tracker.sCenterCoordinatesofObjects[id] = CurrentCenterCoordinates[min_distance_index]
                CurrentCenterCoordinates.pop(min_distance_index)
            
            for center in CurrentCenterCoordinates:
                Tracker.register(center)
           
        elif len(CurrentCenterCoordinates) < len(Tracker.sCenterCoordinatesofObjects):
            updated_id_values = []

            for center in CurrentCenterCoordinates:
                ls = [(id, center, Tracker.computeEuclidianDistance(center, i)) for id, i in Tracker.sCenterCoordinatesofObjects]
                matched_id, matched_center, _ = min(ls, key=lambda x: x[2])
                Tracker.sCenterCoordinatesofObjects[matched_id] = matched_center
                updated_id_values.append(id)

            for id, center in Tracker.sCenterCoordinatesofObjects:
                if id not in updated_id_values:
                    Tracker.deregister(id)

        # nesne sayısı aynı kalmışsa
        else:
            for id, center in Tracker.sCenterCoordinatesofObjects:
                ls = [Tracker.computeEuclidianDistance(center, i) for i in CurrentCenterCoordinates]
                min_distance = min(ls)
                min_distance_index = ls.index(min_distance)
                Tracker.sCenterCoordinatesofObjects[id] = CurrentCenterCoordinates[min_distance_index]

        return Tracker.sCenterCoordinatesofObjects



"""
for id, center in Tracker.sDistancestoObjects.items():
    ls.append([Tracker.computeEuclidianDistance(center, j) for j in CurrentCenterCoordinates])

if len(CurrentCenterCoordinates) > len(Tracker.sCenterCoordinatesofObjects):
    # nesnenin register edilmesi lazım
    pass
elif len(CurrentCenterCoordinates) < len(Tracker.sCenterCoordinatesofObjects):
    # nesnenin deregister edilmesi lazım
    pass
else:
    # koordinatlar arasındaki farklar hesaplansın - euclidian distance
    for i in CurrentCenterCoordinates:
        for j in Tracker.sCenterCoordinatesofObjects:
            Tracker.sDistancestoObjects[i].append(Tracker.computeEuclidianDistance(i, j))
            
            pass
    pass

obj = Tracker()
obj2 = Tracker()
print(obj.id)
print(obj2.id)
"""   

