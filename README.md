# tropopause
Simplify creating AWS CloudFormation templates

## Mission Statement
CloudFormation provides a vast array of options and combinations for your deployment. This can be overwhelming for beginners
and lead to large complicated collections of cfn templates with flow control in them for advanced users.

This library aims to abstract away the more complex and time consuming aspects of building cloudformation templates, in favour
of more common architectures. Although there will be a certain amount of ideology in how I choose to draw the boundaries on
'common' architectures, I will endeavour to keep it extensible; encourage plugins; and always make the underlying [troposphere](https://github.com/cloudtools/troposphere)
objects accessible.

## Assumptions
 - All instances will be contain in auto scaling groups of at least 1.
 
## Plugins
### Extending
In the spirit of loose coupling and reusable code, rather than defining what an instance is meant to be at run time, you
should extend a class which has `compute.Group` in the parent hierarchy. What does this mean?


It means this bad...

    my_web_server = compute.Group(title='WordPress')
    my_web_server.config().packages.update({
        'yum' : {
            'httpd' : [],
            'php' : [],
            'wordpress': []
        }
    })
    my_project.add_computegroup(my_web_server))


And this is good...

    # ~/.tropopause/plugins/mycompany.py
    from tropopause.components import compute
    class Wordpress(compute.Group):
        def __init__(self, **kwargs):
            # Set defaults
            self.php_log_level = None
            self.
            # Initialise Parent
            super().__init__(*kwargs)
            # Override/extend parent
            self.config().packages.update({
                'yum' : {
                    'httpd' : [],
                    'php' : [],
                    'wordpress' : []
                }
            })
            
    # myproject/build_cfn.py
    with plugin_source:
        from mycompany import plugins
    ...
    my_project.add_computegroup(plugins.Wordpress(
        php_log_level=2
    ))
            
            

### Core plugins
#### Compute Groups
compute.Group objects are a wrapper for launch configs, and autoscaling groups.
By wrapping every ami/instance in an autoscaling group, we encourage Highly Available and redundant architectures.
You can create a specific type of ec2 instance (for example a Bastion host) simply be inheriting from this class.

    from troposphere.components import compute
    class WebServer(compute.Group):
        def __init__(self, **kwargs):
            super().__init__(*kwargs)
            