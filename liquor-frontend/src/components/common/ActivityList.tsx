import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Avatar,
  Divider,
} from '@mui/material';
import { motion } from 'framer-motion';

export interface Activity {
  id: number | string;
  user: string;
  action: string;
  time: string;
  avatar?: string;
}

interface ActivityListProps {
  title: string;
  activities: Activity[];
  actionText?: string;
  onActionClick?: () => void;
  maxItems?: number;
  delay?: number;
}

const ActivityList: React.FC<ActivityListProps> = ({
  title,
  activities,
  actionText = 'View All',
  onActionClick,
  maxItems = 5,
  delay = 0,
}) => {
  const displayedActivities = activities.slice(0, maxItems);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay }}
    >
      <Card>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h6" component="h2">
              {title}
            </Typography>
            <Button variant="text" size="small" color="primary" onClick={onActionClick}>
              {actionText}
            </Button>
          </Box>
          <List>
            {displayedActivities.length > 0 ? (
              displayedActivities.map((activity, index) => (
                <React.Fragment key={activity.id}>
                  <ListItem alignItems="flex-start" sx={{ px: 0 }}>
                    <ListItemAvatar>
                      <Avatar alt={activity.user} src={activity.avatar} />
                    </ListItemAvatar>
                    <ListItemText
                      primary={activity.user}
                      secondary={
                        <React.Fragment>
                          <Typography
                            sx={{ display: 'inline' }}
                            component="span"
                            variant="body2"
                            color="text.primary"
                          >
                            {activity.action}
                          </Typography>
                          {` — ${activity.time}`}
                        </React.Fragment>
                      }
                    />
                  </ListItem>
                  {index < displayedActivities.length - 1 && <Divider variant="inset" component="li" />}
                </React.Fragment>
              ))
            ) : (
              <Typography variant="body2" color="textSecondary" sx={{ py: 2, textAlign: 'center' }}>
                No activities to display
              </Typography>
            )}
          </List>
        </CardContent>
      </Card>
    </motion.div>
  );
};

export default ActivityList;