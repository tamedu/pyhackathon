pragma solidity ^0.4.21;


contract ProjectOwnership {

    struct Todo {
        address owner;
        string title;
        address[] approvedParticipants;
        bool approved;
    }

    uint16 public constant TIMMING_UNIT = 1000;
    address[] public participants;
    uint16[] public participantsOwnedTime;
    Todo[] public todos;

    modifier onlyParticipants() {
        require(isParticipated());
        _;
    }

    function version()
    public
    returns (string) {
        return "0.0.1";
    }

    /* todo related functions */
    function approveTodo(uint todoIndex)
    public
    onlyParticipants()
    returns (bool) {
        Todo storage t = todos[todoIndex];
        if (getParticipantId(msg.sender, t.approvedParticipants) > -1) {
            return false;
        } else {
            t.approvedParticipants.push(msg.sender);
            checkTodoApprovement(todoIndex);
            return true;
        }
    }

    function createTodo(string _title)
    public
    onlyParticipants()
    returns (uint) {
        todos.push(Todo({
            owner: msg.sender,
            title: _title,
            approvedParticipants: new address[](0),
            approved: false
        }));
        return todos.length;
    }

    function getTodoInfo(uint256 todoIndex)
    public constant
    onlyParticipants()
    returns (string, address, uint, bool)  {
        Todo storage t = todos[todoIndex];
        return (t.title, t.owner, t.approvedParticipants.length, t.approved);
    }

    /* project related function */
    function join()
    public
    returns (uint) {
        require(!isParticipated());
        participants.push(msg.sender);
        participantsOwnedTime.push(1);
        return participants.length;
    }

    function getParticipantsCount()
    public view
    returns (uint) {
        return participants.length;
    }

    function getTotalTime()
    public view
    returns (uint16) {
        uint16 i = 0;
        uint16 n = 0;
        for (i; i < participants.length; i++) {
            n = n + participantsOwnedTime[i];
        }
        return n;
    }

    function getMyOwnershipPercent()
    public
    onlyParticipants()
    returns (uint16) {
        uint256 myId = uint256(getMyParticipantId());
        uint16 percent = 100 * participantsOwnedTime[myId] / getTotalTime();
        return percent;
    }

    /* private functions go here */
    function checkTodoApprovement(uint256 todoIndex)
    private
    returns (bool) {
        uint256 i = 0;
        uint256 id;
        uint16 total = 0;
        Todo storage t = todos[todoIndex];

        for (i; i < t.approvedParticipants.length; i++) {
            id = uint256(getParticipantId(t.approvedParticipants[i], participants));
            total += participantsOwnedTime[id];
        }
        bool approved = 2 * total > getTotalTime();
        if (t.approved == false && approved == true) {
                uint256 ownerId = uint256(getParticipantId(t.owner, participants));
                t.approved = true;
                participantsOwnedTime[ownerId] += TIMMING_UNIT;
        }
        return approved;
        return t.approved;
    }

    function isParticipated() private view returns (bool) {
        return (getMyParticipantId() > -1);
    }

    function getMyParticipantId()
    private view
    returns (int32) {
        return getParticipantId(msg.sender, participants);
    }

    function getParticipantId(address participant, address[] _participants)
    private view
    returns (int32) {
        uint256 i = 0;
        int32 participantId = -1;

        for (i; i < _participants.length; i++) {
            if (_participants[i] == participant) {
                participantId = int32(i);
                break;
            }
        }
        return participantId;
    }
} // end ProjectOwnership contract
