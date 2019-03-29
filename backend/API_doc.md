## Implemented APIs

#### EventList: `ListCreateAPIView`
* url: `api/event/`;
* Permission: `IsAuthenticatedOrReadOnly`
* `GET` return: list of public(`public=True`) events with fields: `id`, `title`, `host_id`, `host_display_info`, `start_time`, `end_time`, `location`, `require_approve`;
* `POST` require: log-in user (as `host`), along with `title`, `start_time`, `end_time`, `location`, `public`, `require_approve`;

#### [Past|Future|Ongoing]EventList: `ListAPIView`
* url: `api/event/[past|future|ongoing]/`;
* `EventList` with the corresponding filter. Allows only `GET`;

#### UserRegisterEventList: `ListAPIView`
* url: `api/event/registered/`;
* Permission: `IsOwner`;
* `GET` return: list of events registered by the log-in user, with serialized user profile info and transort info.

#### UserRegister[Past|Future|Ongoing]EventList: `ListAPIView`
* url: `api/event/registered/[past|future|ongoing]/`;
* Just `UserRegisterEventList` with filter.

#### UserEventRegister: `CreateAPIView`
* url: `api/register/`;
* Permission: `OpenRegistration|IsEventHostAdmin`;
* `POST`: Register a user to a event (create a `UserRegisterEvent` object). Requires log-in user or specify `user_id` in data, also `event_id` and `transport_id`.
* **Need Testing!!!**

#### AssignEventAdmin: `CreateAPIView`
* url: `api/register/`;
* Permission: `IsEventHostAdmin`;
* `POST`: Assign a user to become event admin (create a `UserManageEvent` object). Requires `user_id`, `event_id` and `transport_id`.
* **Need Testing!!!**

#### EventDetail: `RetrieveUpdateDestroyAPIView`
* url: `api/event/<pk>/`;
* Permission: `IsEventHostAdminOrReadOnly`;
* `GET`: returns event detail plus two fields: `event_admin`, `event_registered` specifing the current log-in user (if any)'s relation to the event.
* **May need further testing**

#### EventAttendeeList: `ListAPIView`
* url: `api/event/<pk>/attendee/`;
* Permission: `IsEventRegistered|IsEventHostAdmin`;
* `GET`: returns the list of serialized `UserRegisterEvent` where `event` is the event specified by `<pk>`.
* **Need Testing!!!**

#### TransportCreateView: `createAPIView`
* url: `api/trans/`;
* Permission: `IsOwner|IsEventHostAdmin`;
* `POST`: Create a `Transport` object, requires all the required field and log-in user or specify `user_id` in data, also `event_id`.


#### TranpostView: `RetrieveUpdateDestroyAPIView`
* url: `api/trans/<pk>/`;
* Permission: `IsOwner|IsEventHostAdmin`;
* **Need Testing!!!**