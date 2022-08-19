import cv2 as cv

class Tracker:
    """
    This is a class for tracking objects based on Euclidian distances
      
    Attributes:
        sNumofObjects (int): Number of tracked objects in the frame
        sCenterCoordinatesofObjects (dict): Center coordinates of tracked objects with their corresponding id's 
    """

    sNumofObjects = 0
    sCenterCoordinatesofObjects = dict()

    def register(self, center):
        """
        The function to register new objects entered frame given their coordinates of the center
    
        Parameters:
            center (tuple): (x, y) coordinate of the object
        """

        Tracker.sNumofObjects += 1
        keys = Tracker.sCenterCoordinatesofObjects.keys()
        for id in range(1, Tracker.sNumofObjects + 1):
            if id not in keys:
                Tracker.sCenterCoordinatesofObjects[id] = center
                break

    def deregister(self, id):
        """
        The function to deregister objects that exited frame given their id
    
        Parameters:
            id (int): id of the object
        """

        Tracker.sNumofObjects -= 1
        Tracker.sCenterCoordinatesofObjects.pop(id)

    @staticmethod
    def computeEuclidianDistance(pt1, pt2):
        """
        The function to compute Euclidian distance between a given two point
    
        Parameters:
            pt1 (tuple): (x, y) coordinates of the first point
            pt2 (tuple): (x, y) coordinates of the second point
        """

        return ((pt1[0] - pt2[0]) ** 2 + (pt1[0] - pt2[0]) ** 2) ** (1/2)

    def update_centers(self, CurrentCenterCoordinates):
        """
        The function to update object's centers in the previous frame given center coordinates of objects in the current frame 
    
        Parameters:
            CurrentCenterCoordinates (list): (x, y) coordinates of detected objects in the current frame

        Returns:
            Tracker.sCenterCoordinatesofObjects (dict): Updated center coordinates of tracked objects with their corresponding id's 
        """

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
        """
        The function to mark centers of tracked objects in the given frame 

        Parameters:
            frame (3-D numpy array): The image over which objects are tracked
        """
        
        for id, center in Tracker.sCenterCoordinatesofObjects.items():
            frame = cv.circle(frame, center, 3, (0, 0, 255), -1)
            frame = cv.putText(frame, "object " + str(id), (center[0], center[1] + 20), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv.LINE_AA)
    
