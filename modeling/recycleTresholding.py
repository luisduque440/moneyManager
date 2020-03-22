    def modelRequiresTraining(self):
        """ 
        To do:
            * Alternative way: many heuristics can be tried here, depending on if/how model is valid working.
        """
        if self.threshold==None and self.modelHasNotBeenTrainedInAWhile():
            return True
        return False


    def getModelThreshold(self):
        """ Returns None if its not possible to satisfy the requirements
            Somehow this piece of the puzzle does not feel entirely right.
            This cannot be right, very careful!!
            Track empty values on yeval, ytrain ... those are key, I bet.
        """
        scores = self.model.predict_proba(self.Xeval)[:,1]
        p,r,threshold,a = selectThreshold(self.yeval, scores, self.requiredPrecision, self.requiredRecall, self.requiredCertainty)
        return threshold

    def thresholdedOutput(self):
        """ Somehow this piece of the puzzle does not feel entirely right.
            This cannot be right, very careful!!
            Track empty values on yeval, ytrain ... those are key, I bet.
            Xeval, yeval, Xtrain, ytrain must be exposed even just for debugging purposes.
        """
        if self.threshold==None: 
            return None
        scores = self.model.predict_proba(self.Xeval)[:,1]
        return scores[-1]>self.threshold


    def generateBuyOrder(self):
        buyOrder =  {
            'orderType': 'BUY', 
            'stock': self.stock,  
            'generatedAt': datetime.now(), 
            'expiresAt': self.currentTime + timedelta(minute=1)
        }
        return buyOrder


    def generateNullOrder(self):
        buyOrder =  {
            'orderType': 'NULL', 
            'stock': self.stock,  
            'generatedAt': datetime.now(), 
            'expiresAt': self.currentTime + timedelta(minute=1)
        }
        return buyOrder

