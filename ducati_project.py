# !/usr/bin/python2.7
# coding=utf-8
#######################################################################
# ------------------  Ducati Summer School   ------------------------ #
#                                                                     #
# This program is the simulation of a research done during the        #
# Ducati Summer School on July 2019.                                  #
# The research goal was the studying of the variation of a biker's    #
# angular velocity during a curve. The study was done through the use #
# of a carousel which rotated around an axe. This carousel could move #
# forward and backward relative to the axe, simulating the bend of a  #
# biker during the curve.                                             #
#                                                                     #
# For more information read the files inside doc folder.              #
#                                                                     #
# Research team:                                                      #
# - Lorenzo Calandra Buonaura                                         #
# - Fabiola Borsci                                                    #
# - Alexandru Burlacu                                                 #
# - Edoardo Carrà                                                     #
# - Leonardo Zecchinelli                                              #
#                                                                     #
# developed by Edoardo Carrà                                          #
#                                                                     #
#######################################################################

import math
import time
import pygraph.pyig as ig

black = "#000000"


class Timer:
    """Timer for the execution of the simulation(handle the pause and the restart)."""

    def __init__(self):
        self._init_time = time.time()

        # time which isn't counted
        self._do_not_count = 0
        self._start_c = 0
        # if the timer is pause
        self.is_in_pause = False

    def set_init_time(self):
        """Set the initial time of the simulation."""

        self.is_in_pause = False
        self._do_not_count = 0
        self._init_time = time.time()

    def pause(self):
        """Pause the timer."""

        self._start_c = time.time()
        self.is_in_pause = True

    def restart(self):
        """Restart the timer."""

        self._do_not_count += time.time() - self._start_c
        self.is_in_pause = False

    def get_time_passed(self):
        """Time has been passed since the simulation starting(from last set_init_time)."""

        if self.is_in_pause:
            return self._start_c - self._init_time - self._do_not_count
        else:
            return time.time() - self._init_time - self._do_not_count


class Model:
    """Model of the project(see the CHE COSAAAgfdstrwaaegsdtgrdtrthrytrteertytreretryrtrrtrytrrertyrfhf)"""

    def __init__(self, ray, distance, w, translation_velocity):
        """
        :param ray: Ray of the curve
        :type ray: float
        :param distance: Distance between the ground and the barycenter of the bike+biker
        :type distance: float
        :param w: Initial angular velocity
        :type w: float
        :param translation_velocity: Translation velocity of the carousel
        :type translation_velocity: float
        """

        self.ray = ray
        self.distance = distance
        self.w = w
        self.translation_velocity = translation_velocity

    def ray_at(self, time_passed=0.0):
        """The ray of the curve as a function of the translation velocity of the carousel

        :param time_passed: Time passed since the beginning of the simulation
        :type time_passed: float
        :return: The ray at time given
        :rtype: float
        """

        return self.ray - self.translation_velocity * time_passed

    def angle_at(self, time_passed=0.0):
        """The angle in degrees of bend as a function of the translation velocity of the carousel

        :param time_passed: Time passed since the beginning of the simulation
        :type time_passed: float
        :return: The angle of bend at given time
        :rtype: float
        """

        return Model.to_degree(math.asin((self.ray - self.ray_at(time_passed))/self.distance))

    def angle_radians_at(self, time_passed=0.0):
        """The angle in radians of bend as a function of the translation velocity of the carousel

        :param time_passed: Time passed since the beginning of the simulation
        :type time_passed: float.
        :return: The angle in radians of bend at given time.
        :rtype: float
        """

        return math.asin((self.ray - self.ray_at(time_passed))/self.distance)

    def w_at(self, time_passed=0):
        """The angular velocity, relative to the curve, of the carousel and the bike

        :param time_passed: Time passed since the beginning of the simulation
        :type time_passed: float
        :return: The angular velocity of the carousel at given time
        :rtype: float
        """

        return self.w*self.ray/self.ray_at(time_passed)

    def angle_traveled(self, time_passed=0.0):
        """The angle traveled as a function of angular velocity relative to the curve

        :param time_passed: Time passed since the beginning of the simulation
        :type time_passed: float
        :return: The angle traveled by the carousel
        :rtype: float
        """

        return (self.w*self.ray/self.ray_at(time_passed))*time_passed

    def w_bend_at(self, time_passed=0.0):
        """The angular velocity as a function of the translation velocity of the carousel

        :param time_passed: Time passed since the beginning of the simulation
        :type time_passed: float
        :return: The angular velocity of bend at given time
        :rtype: float
        """

        return self.translation_velocity / (math.cos(self.angle_radians_at(time_passed))*self.distance)

    def maximum_w_bend(self):
        """The maximum angular velocity of bend at 90 degrees of bend with the carousel configuration

        :return: The maximum angular velocity of bend at 90 degrees of bend
        :rtype: float
        """

        return self.translation_velocity / (math.cos(Model.to_radian(89.99999)) * self.distance)

    def maximum_angle_traveled(self, time_passed=0.0):
        """The maximum angle traveled by carousel at 90 degrees of bend

        :param time_passed: Time passed since the beginning of the simulation
        :type time_passed: float
        :return: The maximum angle traveled by carousel at 90 degrees of bend
        :rtype: float
        """

        return (self.w*self.ray/(self.ray-self.distance)) * time_passed

    def minimum_ray(self):
        """The minimum ray reach at 90 degrees of bend

        :return: The minimum ray reach at 90 degrees of bend
        :rtype: float
        """

        return self.ray-self.distance

    def initial_angle(self, r):
        """work in progress

        :param r: The ray of the curve
        :type r: float
        :return: The initial angle of the bike
        :rtype: float
        """

        return math.atan(self.w*self.w*9.81/r)

    @staticmethod
    def to_degree(angle):
        """Converts radians angle in degrees

        :param angle: Angle in radians
        :type angle: float
        :return: The angle given in degrees
        :rtype: float
        """

        return angle*180/math.pi

    @staticmethod
    def to_radian(angle):
        """Converts degrees angle in radians

        :param angle: Angle in degrees
        :type angle: float
        :return: The angle given in radians
        :rtype: float
        """

        return angle*math.pi/180


class Control:
    """This class provides several methods to handle events generated by the view"""

    def __init__(self, model):
        """
        :param model: A model to insert inside the view
        :type model: Model
        """

        self._model = model

        # anchors to a view object
        self._view = View(self._model.ray, self._model.distance)
        self._timer = Timer()
        self._view.show(self)

    def start_simulation_listener(self, event):
        """Updates the view in loop after a view key-pressed event

        :param event: Not used
        """

        self._timer.set_init_time()
        current_time = self._timer.get_time_passed()
        while self._model.ray - self._model.ray_at(current_time) < self._model.distance:
            # update the parameters of the visual
            self._view.update_parameters(current_time, self._model.w_at(current_time),
                                         self._model.angle_at(current_time),
                                         self._model.w_bend_at(current_time), self._model.ray_at(current_time))
            # angle traveled by the carousel
            angle = Model.to_degree(self._model.angle_traveled(current_time))
            # angle of bend
            angle_biker = 90 + self._model.angle_at(current_time)
            # intersection parameter
            which = -1

            # the position of the two points which give the direction
            if angle % 360 == 90 or angle_biker == 90:
                x, y = 0, 1
                x_biker, y_biker = 0, 1
            elif angle % 360 == 270:
                x, y = 0, -1
            elif angle % 360 == 180 or angle_biker == 180:
                x, y = -1, 0
                x_biker, y_biker = -1, 0
            else:
                x, y = 1, math.tan(Model.to_radian(angle))
                x_biker, y_biker = 1, math.tan(Model.to_radian(angle_biker))

            if 90 < angle % 360 < 270 and angle % 360 != 180:
                which = 1

            # update the view
            self._view.update_views(new_ray=self._model.ray_at(current_time),
                              which=which, rotation_point_x=x, rotation_point_y=y, biker_rotation_point_x=x_biker,
                              biker_rotation_point_y=y_biker)
            current_time = self._timer.get_time_passed()

        # updates the parameters with 90° bend
        self._view.update_parameters(current_time, self._model.w_at(current_time),
                                     90, self._model.maximum_w_bend(), self._model.minimum_ray())
        # angle traveled by the carousel
        angle = Model.to_degree(self._model.maximum_angle_traveled(current_time))
        # angle of bend
        x_biker, y_biker = 1, 0
        # intersection parameter
        which = -1

        # the position of the two points which give the direction
        if angle % 360 == 90:
            x, y = 0, 1
        elif angle % 360 == 270:
            x, y = 0, -1
        elif angle % 360 == 180:
            x, y = -1, 0
        else:
            x, y = 1, math.tan(Model.to_radian(angle))

        if 90 < angle % 360 < 270 and angle % 360 != 180:
            which = 1

        # updates the view
        self._view.update_views(new_ray=self._model.minimum_ray(), which=which, rotation_point_x=x, rotation_point_y=y,
                                biker_rotation_point_x=x_biker, biker_rotation_point_y=y_biker)

    def pause_listener(self, event):
        """Handles the pause and restart event.

        :param event: Not used
        """
        
        if self._timer.is_in_pause:
            self._timer.restart()
        else:
            self._timer.pause()


class View:
    """This class defines two views:
        -The first is the view from above of the the carousel;
        -The second is the view from the front of the biker which bends"""
    
    def __init__(self, ray, ray_biker):
        """
        :param ray: The ray of the curve
        :type ray: float
        :param ray_biker: The distance between the ground and the bike+biker barycenter
        :type ray_biker: float
        """
        
        self._ip = ig.InteractivePlane('Ducati Summer School-la giostra', sy=200, sx=200, w=1200, h=600)

        self._ray_curve = ig.Point(ray, 0, visible=False)
        self._center_circle = ig.Point(0, 0, visible=False)
        self._rotation_axe = ig.Point(0, 0, width=6, name='asse di\n rotazione', color=black)

        self._timer = ig.Text(-1.5, 1.3, "time passed:0", color=black, width=15)
        self._w_text = ig.Text(-1.5, 1.15, "angular velocity:0", color=black, width=15)
        self._ray_text = ig.Text(-1.5, 1, "distance from rotation axe:"+str(ray), color=black, width=15)

        self._rotation_point = ig.Point(1, 1, visible=False)
        self._curve_trajectory = ig.Circle(self._center_circle, self._ray_curve)
        self._angle_trajectory = ig.Line(self._rotation_point, self._center_circle, visible=False)

        self._bike_barycenter = ig.Intersection(self._angle_trajectory, self._curve_trajectory, -1, width=10,
                                                name='baricentro moto+pilota')
        self._counterweight_barycenter = ig.Intersection(self._angle_trajectory, self._curve_trajectory, 1, width=10,
                                                         name='baricentro contrappeso')
        self._link_axe = ig.Segment(self._bike_barycenter, self._counterweight_barycenter, color=black)

        #########
        # biker #
        #########
        self._ip_biker = ig.InteractivePlane(name="biker visual", sy=450, sx=450, ox=499, oy=449, h=450, w=500)
        self._ray_curve_biker = ig.Point(ray_biker, 0, visible=False, iplane=self._ip_biker)
        self._center_circle_biker = ig.Point(0, 0, visible=False, iplane=self._ip_biker)
        self._rotation_axe_biker = ig.Point(0, 0, width=6, name='contatto ruota-asfalto', color=black,
                                             iplane=self._ip_biker)

        self._timer_biker = ig.Text(-0.7, 0.9, "time passed:0", color=black, width=15, iplane=self._ip_biker)
        self._angle_text = ig.Text(-0.7, 0.85, "angle of biker:0", color=black, width=15, iplane=self._ip_biker)
        self._w_bend_text = ig.Text(-0.7, 0.8, "angular velocity of bend:0", color=black, width=15,
                                    iplane=self._ip_biker)

        self._rotation_point_biker = ig.Point(-1, 1, visible=False, iplane=self._ip_biker)
        self._curve_trajectory_biker = ig.Circle(self._center_circle_biker, self._ray_curve_biker)
        self._angle_trajectory_biker = ig.Line(self._rotation_point_biker, self._center_circle_biker, visible=False)

        self._bike_barycenter_biker = ig.Intersection(self._angle_trajectory_biker, self._curve_trajectory_biker, -1,
                                                      width=10, name='baricentro moto')
        self._start_bend = ig.Point(0, ray_biker, visible=False)
        self._angle_of_bend = ig.Angle(self._start_bend, self._center_circle_biker, self._bike_barycenter_biker,
                                       width=10, color="red")
        self._angle_side = ig.Segment(self._center_circle_biker, self._bike_barycenter_biker, color="red")
        self._angle_label = ig.Label(self._angle_of_bend, -30.1, 30.2, self._angle_of_bend.extent(), color="black")

    def update_parameters(self, time_passed, w, angle, w_bend, ray):
        """Updates the parameters of the two views
        
        :param time_passed: Time passed since the beginning of the simulation
        :type time_passed: float
        :param w: Angular velocity of the carousel
        :type w: float
        :param angle: Angle of bend
        :type angle: float
        :param w_bend: Angular velocity of bend
        :type w_bend: float 
        :param ray: Distance between the projection of the barycenter and the axe of rotation
        :type ray: float
        """
        
        ############
        # carousel #
        ############
        self._timer.visible = False
        self._timer = ig.Text(-1.5, 1.3, "time passed:"+str(time_passed), color=black, width=15, iplane=self._ip)
        self._w_text.visible = False
        self._w_text = ig.Text(-1.5, 1.15, "angular velocity:" + str(w), color=black, width=15, iplane=self._ip)
        self._ray_text.visible = False
        self._ray_text = ig.Text(-1.5, 1, "distance from rotation axe:"+str(ray), color=black, width=15,
                                 iplane=self._ip)
        #########
        # biker #
        #########
        self._timer_biker.visible = False
        self._timer_biker = ig.Text(-0.7, 0.9, "time passed:" + str(time_passed), color=black, width=15,
                                    iplane=self._ip_biker)
        self._angle_text.visible = False
        self._angle_text = ig.Text(-0.7, 0.85, "angle of biker:" + str(angle), color=black, width=15,
                                   iplane=self._ip_biker)
        self._w_bend_text.visible = False
        self._w_bend_text = ig.Text(-0.7, 0.8, "angular velocity of bend:" + str(w_bend), color=black, width=15,
                                    iplane=self._ip_biker)

    def update_views(self, new_ray, which, rotation_point_x, rotation_point_y, biker_rotation_point_x,
                     biker_rotation_point_y):
        """Updates the objects of the view.

        :param new_ray: The new ray of the circle inside the carousel view
        :type new_ray: float
        :param which: Which intersection between the line and the circle(-1 or 1)
        :type which: int
        :param rotation_point_x: X coordinate of the point which gives the inclination of the line inside the carousel
                                 view
        :type rotation_point_x: float
        :param rotation_point_y: Y coordinate of the point which gives the inclination of the line inside the carousel
                                 view
        :type rotation_point_y: float
        :param biker_rotation_point_x: X coordinate of the point which gives the inclination of the line inside the
                                       biker view
        :type biker_rotation_point_x: float
        :param biker_rotation_point_y: Y coordinate of the point which gives the inclination of the line inside the
                                       biker view
        :type biker_rotation_point_y: float
        """
        # set invisible the old objects
        #########
        # biker #
        #########
        self._bike_barycenter_biker.visible = False
        self._bike_barycenter_biker.name = ""
        self._angle_of_bend.visible = False
        self._angle_side.visible = False
        self._rotation_point_biker = ig.Point(biker_rotation_point_x, biker_rotation_point_y,
                                              visible=False, iplane=self._ip_biker)
        self._angle_trajectory_biker = ig.Line(self._rotation_point_biker, self._center_circle_biker, visible=False)

        self._bike_barycenter_biker = ig.Intersection(self._angle_trajectory_biker, self._curve_trajectory_biker, 1,
                                                      width=10, name='baricentro moto')
        self._angle_of_bend = ig.Angle(self._start_bend, self._center_circle_biker, self._bike_barycenter_biker,
                                       width=10, color="red")
        self._angle_side = ig.Segment(self._center_circle_biker, self._bike_barycenter_biker, color="red")

        ############
        # carousel #
        ############
        self._curve_trajectory.visible = False
        self._angle_trajectory.visible = False
        self._bike_barycenter.visible = False
        self._bike_barycenter.name = ""
        self._counterweight_barycenter.visible = False
        self._counterweight_barycenter.name = ""
        self._link_axe.visible = False
        self._angle_label.visible = False

        self._ray_curve = ig.Point(new_ray, 0, visible=False, iplane=self._ip)
        self._rotation_point = ig.Point(rotation_point_x, rotation_point_y, visible=False, iplane=self._ip)
        self._curve_trajectory = ig.Circle(self._center_circle, self._ray_curve)
        self._angle_trajectory = ig.Line(self._rotation_point, self._center_circle, visible=False)
        self._bike_barycenter = ig.Intersection(self._angle_trajectory, self._curve_trajectory, which,
                                                width=10, name='baricentro moto')
        self._counterweight_barycenter = ig.Intersection(self._angle_trajectory, self._curve_trajectory, -which,
                                                         width=10, name='baricentro contrappeso')

        self._link_axe = ig.Segment(self._bike_barycenter, self._counterweight_barycenter, color=black)
        self._angle_label = ig.Label(self._angle_of_bend, -30.1, 30.2, self._angle_of_bend.extent(), color="black")
        self._ip.getcanvas().update()

    def show(self, ctrl):
        """Shows the two views and sets the event listeners

        :param ctrl: The control object which has got the event listeners
        :type ctrl: Control
        """
        self._ip.onkeypress(ctrl.start_simulation_listener)
        self._ip.onpress3(ctrl.pause_listener)
        self._ip_biker.onkeypress(ctrl.start_simulation_listener)
        self._ip_biker.onpress3(ctrl.pause_listener)
        self._ip.mainloop()


def main():
    simulation = Model(1.41, 0.8, 2.39, 0.12)
    control = Control(simulation)


if __name__=="__main__":
    main()
