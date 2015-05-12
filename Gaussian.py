import scipy.stats
import math

class Gaussian:
    def __init__(self,mean=0,var=0):
    
        self.dis = scipy.stats.norm(mean,math.sqrt(var))
        self.mean = mean
        self.var = var

    def __str__(self):
        return "Mean is "+ str(self.mean)+" and variance is "+str(self.var)

    def __eq__(self,operant):
        if(self.mean == operant.mean and self.var == operant.var):
            return True
        else:
            return False
    def pdf(self,value):
        return self.dis.pdf(value)

    def phi(self,value):
        return self.dis.cdf(value)

    @staticmethod
    def pdf(value):
        return scipy.stats.norm.pdf(value)

    @staticmethod
    def phi(value):
        return scipy.stats.norm.cdf(value)

    def __add__(self,operant):
        return Gaussian(self.mean+operant.mean,self.var+operant.var)

    def __sub__(self,operant):
        return Gaussian(self.mean-operant.mean,self.var-operant.var)

    def __mul__(self,operant):
        if(self.var == 0):
            return operant
        elif(operant.var == 0 ):
            return self
        else:
            newVar = 1.0/(1.0/self.var + 1.0/operant.var)
            newMean = (self.mean/self.var + operant.mean/operant.var)*newVar
            return Gaussian(newMean,newVar)

        

    def __div__(self,operant):
        if(operant.var==0):
            return self
        elif(self.mean == operant.mean and self.var == operant.var):
            return Gaussian();
        else:
            newVar = 1.0/(1.0/self.var - 1.0/operant.var)
            newMean = (self.mean/self.var - operant.mean/operant.var)*newVar
            return Gaussian(newMean,newVar)
        
if __name__=="__main__":
    print Gaussian(0,1)/Gaussian(0,2)
