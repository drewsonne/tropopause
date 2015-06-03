# tropopause
Simplify creating AWS CloudFormation templates

## Mission Statement
CloudFormation provides a vast array of options and combinations for your deployment. As a starting point, you usually just want
something simple. 

This library aims to abstract away the more complex and time consuming aspects of building cloudformation templates, in favour
of more common architectures. Although there will be a certain amount of ideology in how I choose to draw the boundaries on
'common' architectures, I will endeavour to keep it extensible; encourage plugins; and always make the underlying [troposphere](https://github.com/cloudtools/troposphere)
objects accessible.

## Assumptions
 - All instances will be contain in auto scaling groups of at least 1.
 
## Plugins
### Compute Groups
compute.Group objects are a wrapper for launch configs, and autoscaling groups.
By wrapping every ami/instance in an autoscaling group, we encourage Highly Available and redundant architectures.