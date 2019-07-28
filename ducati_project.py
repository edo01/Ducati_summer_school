# coding=utf-8
##########################################
# ----------ducati project-------------- #
#                                        #
#                                        #
# developed by Edoardo Carrà             #
#                                        #
##########################################

import math
import time
import pygraph.pyig as ig

black = "#000000"


class Timer:
    def __init__(self):
        self._init_time = time.time()
        self._do_not_count = 0
        self._start_c = 0
        self.pause = False

    def set_init_time(self):
        self.pause = False
        self._do_not_count = 0
        self._init_time = time.time()

    def stop(self):
        self._start_c = time.time()
        self.pause = True

    def restart(self):
        self._do_not_count += time.time() - self._start_c
        self.pause = False

    def get_time_passed(self):
        if self.pause:
            return self._start_c - self._init_time - self._do_not_count
        else:
            return time.time() - self._init_time - self._do_not_count


class Model:
    def __init__(self, ray, distance, w, translation_velocity):

        # ray of the curve
        self.ray = ray

        # distance between the ground and the barycenter of the bike+biker
        self.distance = distance

        # initial angular velocity
        self.w = w

        # velocity of the carousel
        self.translation_velocity = translation_velocity

    # 1
    def ray_at(self, time_passed=0.0):
        return self.ray - self.translation_velocity * time_passed

    # 2
    def angle_at(self, time_passed=0.0):
        return Model.to_degree(math.asin((self.ray - self.ray_at(time_passed))/self.distance))

    # 2
    def angle_radians_at(self, time_passed=0.0):
        return math.asin((self.ray - self.ray_at(time_passed))/self.distance)

    # 3
    def w_at(self, time_passed=0):
        return self.w*self.ray/self.ray_at(time_passed)
    #    return self.translation_velocity/((self.ray_at(time_passed)/self.distance)*self.ray)

    # 4
    def angle_traveled(self, time_passed=0.0):
        # print("velocity:", self.w*self.ray/self.ray_at(time_passed), "; angle done:",
        #      Model.to_degree((self.w*self.ray/self.ray_at(time_passed))*time_passed), " after:", time_passed)
        return (self.w*self.ray/self.ray_at(time_passed))*time_passed

    # 5
    def w_bend_at(self, time_passed=0.0):
        return self.translation_velocity / (math.cos(self.angle_radians_at(time_passed))*self.distance)

    def maximum_w_bend(self):
        return self.translation_velocity / (math.cos(Model.to_radian(89.99999))*self.distance)

    def maximum_angle_traveled(self):
        return self.w*self.ray/(self.ray-self.distance)

    def minimum_ray(self):
        return self.ray-self.distance

    @staticmethod
    def to_degree(angle):
        return angle*180/math.pi

    @staticmethod
    def to_radian(angle):
        return angle*math.pi/180


class Control:

    def __init__(self, model):
        self._model = model
        self._view = View(self._model.ray, self._model.distance)
        self._timer = Timer()
        self._view.show(self)

    def update(self, event):
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
            self._view.update(new_ray=self._model.ray_at(current_time),
                              which=which, rotation_point_x=x, rotation_point_y=y, biker_rotation_point_x=x_biker,
                              biker_rotation_point_y=y_biker)
            current_time = self._timer.get_time_passed()

        # update the parameters with 90° bend
        self._view.update_parameters(current_time, self._model.w_at(current_time),
                                     90, self._model.maximum_w_bend(), self._model.minimum_ray())
        # angle traveled by the carousel
        angle = Model.to_degree(self._model.maximum_angle_traveled())
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

        # update the view
        self._view.update(new_ray=self._model.minimum_ray(),
                          which=which, rotation_point_x=x, rotation_point_y=y, biker_rotation_point_x=x_biker,
                          biker_rotation_point_y=y_biker)

    def timer_event(self, event):
        if self._timer.pause:
            self._timer.restart()
        else:
            self._timer.stop()


class View:
    def __init__(self, ray, ray_biker):
        self._ip = ig.InteractivePlane('Ducati Summer School-la giostra', sy=200, sx=200, w=1200, h=600)

        self._ray_curve = ig.Point(ray, 0, visible=False)
        self._center_circle = ig.Point(0, 0, visible=False)
        self._rotation_axis = ig.Point(0, 0, width=6, name='asse di\n rotazione', color=black)

        self._timer = ig.Text(-1.5, 1.3, "time passed:0", color=black, width=15)
        self._w_text = ig.Text(-1.5, 1.15, "angular velocity:0", color=black, width=15)
        self._ray_text = ig.Text(-1.5, 1, "distance from rotation axis:"+str(ray), color=black, width=15)

        self._rotation_point = ig.Point(1, 1, visible=False)
        self._curve_trajectory = ig.Circle(self._center_circle, self._ray_curve)
        self._angle_trajectory = ig.Line(self._rotation_point, self._center_circle, visible=False)

        self._bike_barycenter = ig.Intersection(self._angle_trajectory, self._curve_trajectory, -1, width=10,
                                                name='baricentro moto+pilota')
        self._counterweight_barycenter = ig.Intersection(self._angle_trajectory, self._curve_trajectory, 1, width=10,
                                                         name='baricentro contrappeso')
        self._link_axis = ig.Segment(self._bike_barycenter, self._counterweight_barycenter, color=black)

        #########
        # biker #
        #########
        self._ip_biker = ig.InteractivePlane(name="biker visual", sy=450, sx=450, ox=499, oy=449, h=450, w=500)
        self._ray_curve_biker = ig.Point(ray_biker, 0, visible=False, iplane=self._ip_biker)
        self._center_circle_biker = ig.Point(0, 0, visible=False, iplane=self._ip_biker)
        self._rotation_axis_biker = ig.Point(0, 0, width=6, name='contatto ruota-asfalto', color=black,
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

        ############
        # carousel #
        ############
        self._timer.visible = False
        self._timer = ig.Text(-1.5, 1.3, "time passed:"+str(time_passed), color=black, width=15, iplane=self._ip)
        self._w_text.visible = False
        self._w_text = ig.Text(-1.5, 1.15, "angular velocity:" + str(w), color=black, width=15, iplane=self._ip)
        self._ray_text.visible = False
        self._ray_text = ig.Text(-1.5, 1, "distance from rotation axis:"+str(ray), color=black, width=15,
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

    def update(self, new_ray, which, rotation_point_x, rotation_point_y, biker_rotation_point_x,
               biker_rotation_point_y):
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
        self._link_axis.visible = False
        self._angle_label.visible = False

        self._ray_curve = ig.Point(new_ray, 0, visible=False, iplane=self._ip)
        self._rotation_point = ig.Point(rotation_point_x, rotation_point_y, visible=False, iplane=self._ip)
        self._curve_trajectory = ig.Circle(self._center_circle, self._ray_curve)
        self._angle_trajectory = ig.Line(self._rotation_point, self._center_circle, visible=False)
        self._bike_barycenter = ig.Intersection(self._angle_trajectory, self._curve_trajectory, which,
                                                width=10, name='baricentro moto')
        self._counterweight_barycenter = ig.Intersection(self._angle_trajectory, self._curve_trajectory, -which,
                                                         width=10, name='baricentro contrappeso')

        self._link_axis = ig.Segment(self._bike_barycenter, self._counterweight_barycenter, color=black)
        print(self._angle_of_bend.extent())
        self._angle_label = ig.Label(self._angle_of_bend, -30.1, 30.2, self._angle_of_bend.extent(), color="black")
        self._ip.getcanvas().update()

    def show(self, ctrl):
        self._ip.onkeypress(ctrl.update)
        self._ip.onpress3(ctrl.timer_event)
        self._ip_biker.onpress3(ctrl.timer_event)
        self._ip_biker.onkeypress(ctrl.update)
        self._ip.mainloop()


simulation = Model(1.41, 0.8, 2.39, 0.12)
control = Control(simulation)
