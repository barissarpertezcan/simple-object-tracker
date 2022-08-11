import cv2 as cv

class Tracker:
    sNumofObjects = 0
    sCenterCoordinatesofObjects = dict()

    def register(self, center):
        Tracker.sNumofObjects += 1
        keys = Tracker.sCenterCoordinatesofObjects.keys()
        for id in range(1, Tracker.sNumofObjects + 1):
            if id not in keys:
                Tracker.sCenterCoordinatesofObjects[id] = center
                break

    def deregister(self, id):
        Tracker.sNumofObjects -= 1
        Tracker.sCenterCoordinatesofObjects.pop(id)

    @staticmethod
    def computeEuclidianDistance(pt1, pt2):
        return ((pt1[0] - pt2[0]) ** 2 + (pt1[0] - pt2[0]) ** 2) ** (1/2)

    def update_centers(self, CurrentCenterCoordinates):
        # number of objects is less than the number of objects in the previous frame 
        if len(CurrentCenterCoordinates) > len(Tracker.sCenterCoordinatesofObjects):
            for id, center in Tracker.sCenterCoordinatesofObjects.items():
                ls = [Tracker.computeEuclidianDistance(center, i) for i in CurrentCenterCoordinates]
                min_distance = min(ls)
                min_distance_index = ls.index(min_distance)
                Tracker.sCenterCoordinatesofObjects[id] = CurrentCenterCoordinates[min_distance_index]
                CurrentCenterCoordinates.pop(min_distance_index)
            
            for center in CurrentCenterCoordinates:
                self.register(center)

        # number of objects is more than the number of objects in the previous frame 
        elif len(CurrentCenterCoordinates) < len(Tracker.sCenterCoordinatesofObjects):
            updated_id_values = []

            for center in CurrentCenterCoordinates:
                ls = [(id, center, Tracker.computeEuclidianDistance(center, i)) for id, i in Tracker.sCenterCoordinatesofObjects.items()]
                matched_id, matched_center, _ = min(ls, key=lambda x: x[2])
                Tracker.sCenterCoordinatesofObjects[matched_id] = matched_center
                updated_id_values.append(matched_id)

            for id in list(Tracker.sCenterCoordinatesofObjects.keys()):
                if id not in updated_id_values:
                    self.deregister(id)
                    #print("----deregistering----")
                    #print(Tracker.sNumofObjects)

        # number of objects stays same 
        else:
            for id, center in Tracker.sCenterCoordinatesofObjects.items():
                ls = [Tracker.computeEuclidianDistance(center, i) for i in CurrentCenterCoordinates]
                min_distance = min(ls)
                min_distance_index = ls.index(min_distance)
                Tracker.sCenterCoordinatesofObjects[id] = CurrentCenterCoordinates[min_distance_index]

        return Tracker.sCenterCoordinatesofObjects

    def draw_centers(self, frame):
        for id, center in Tracker.sCenterCoordinatesofObjects.items():
            frame = cv.circle(frame, center, 3, (0, 0, 255), -1)
            frame = cv.putText(frame, "object " + str(id), (center[0], center[1] + 20), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv.LINE_AA)
    
