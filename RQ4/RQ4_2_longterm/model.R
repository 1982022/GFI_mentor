library("corrplot")
library("e1071")
library('mgcv')
library("reshape")
library("generalhoslem")

a<-read.csv(file="info.csv", header = TRUE, sep = ",")
a <- a[complete.cases(a),]
summary(a)
b<-cor(a[,3:15], method= "spearman")
corrplot(b)
corrplot(b, method = "number", type = "upper", tl.cex = 1) 
corrplot(b,method="color",addCoef.col="grey") 
#cor.test(a$num_url, a$count_word_title, alternative = "two.sided",method = "spearman",exact=FALSE, conf.level = 0.95)

model.final = glm(sustain ~ log(expert_comments+1) + log(newcomer_comments+1) + log(duration+1) + 
                   log(stars+1) + log(commits) + log(labels) + log(age) + log(files) + mentorship_network + expert_involvement,
                  data = a, 
                  family = binomial(link ="logit"), 
                  na.action(na.omit))

summary(model.final)

model1.final = glm(sustain ~ log(newcomer_comments+1) + log(stars+1) +  log(files) + expert_involvement,
                                 data = a, 
                                 family = binomial(link ="logit"), 
                                 na.action(na.omit))

summary(model1.final)

#hoslem_gof(model.final)

nullmod <- glm(sustain~1, data = a, family = binomial(link ="logit"), na.action(na.omit))
1-logLik(model1.final)/logLik(nullmod)




